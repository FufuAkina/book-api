import pytest
from httpx import AsyncClient

# ========== 测试图书查询 ==========

@pytest.mark.asyncio
async def test_get_books_empty(client: AsyncClient):
    """测试获取空图书列表"""
    response = await client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["items"] == []

@pytest.mark.asyncio
async def test_create_book_success(client: AsyncClient, auth_headers):
    """测试创建图书（已登录）"""
    book_data = {
        "title": "测试图书",
        "author": "测试作者",
        "isbn": "9781234567890",
        "price": 59.00,
        "description": "测试描述"
    }
    response = await client.post("/books", json=book_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试图书"
    assert data["author"] == "测试作者"
    assert data["id"] is not None

@pytest.mark.asyncio
async def test_create_book_unauthorized(client: AsyncClient):
    """测试未登录无法创建图书"""
    book_data = {
        "title": "测试图书",
        "author": "测试作者",
        "isbn": "9781234567890",
        "price": 59.00,
    }
    response = await client.post("/books", json=book_data)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_book_duplicate_isbn(client: AsyncClient, auth_headers):
    """测试重复 ISBN 无法创建"""
    book_data = {
        "title": "图书1",
        "author": "作者1",
        "isbn": "9781111111111",
        "price": 50.00,
    }
    # 第一次创建成功
    response1 = await client.post("/books", json=book_data, headers=auth_headers)
    assert response1.status_code == 201
    
    # 第二次创建失败（ISBN 重复）
    book_data["title"] = "图书2"
    response2 = await client.post("/books", json=book_data, headers=auth_headers)
    assert response2.status_code == 400
    assert "已存在" in response2.json()["detail"]

@pytest.mark.asyncio
async def test_get_book_by_id(client: AsyncClient, auth_headers):
    """测试根据 ID 获取图书"""
    # 先创建
    book_data = {
        "title": "Python编程",
        "author": "作者",
        "isbn": "9782222222222",
        "price": 89.00,
    }
    create_response = await client.post("/books", json=book_data, headers=auth_headers)
    book_id = create_response.json()["id"]
    
    # 再查询
    response = await client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Python编程"
    assert data["id"] == book_id

@pytest.mark.asyncio
async def test_get_book_not_found(client: AsyncClient):
    """测试获取不存在的图书"""
    response = await client.get("/books/99999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_book_success(client: AsyncClient, auth_headers):
    """测试更新图书"""
    # 先创建
    book_data = {
        "title": "原标题",
        "author": "原作者",
        "isbn": "9783333333333",
        "price": 50.00,
    }
    create_response = await client.post("/books", json=book_data, headers=auth_headers)
    book_id = create_response.json()["id"]
    
    # 更新
    update_data = {
        "title": "新标题",
        "author": "原作者",
        "isbn": "9783333333333",
        "price": 99.00,
    }
    response = await client.put(f"/books/{book_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "新标题"
    assert data["price"] == 99.00

@pytest.mark.asyncio
async def test_update_book_unauthorized(client: AsyncClient):
    """测试未登录无法更新图书"""
    update_data = {
        "title": "新标题",
        "author": "作者",
        "isbn": "9784444444444",
        "price": 60.00,
    }
    response = await client.put("/books/1", json=update_data)
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_delete_book_forbidden_for_normal_user(client: AsyncClient, auth_headers):
    """测试普通用户无法删除图书"""
    # 先创建
    book_data = {
        "title": "待删除图书",
        "author": "作者",
        "isbn": "9785555555555",
        "price": 40.00,
    }
    create_response = await client.post("/books", json=book_data, headers=auth_headers)
    book_id = create_response.json()["id"]
    
    # 尝试删除（普通用户）
    response = await client.delete(f"/books/{book_id}", headers=auth_headers)
    assert response.status_code == 403
    assert "管理员" in response.json()["detail"]

@pytest.mark.asyncio
async def test_delete_book_success_for_admin(client: AsyncClient, admin_headers, auth_headers):
    """测试管理员可以删除图书"""
    # 先创建（用普通用户创建）
    book_data = {
        "title": "待删除图书",
        "author": "作者",
        "isbn": "9786666666666",
        "price": 40.00,
    }
    create_response = await client.post("/books", json=book_data, headers=auth_headers)
    book_id = create_response.json()["id"]
    
    # 管理员删除
    response = await client.delete(f"/books/{book_id}", headers=admin_headers)
    assert response.status_code == 200
    
    # 验证已删除
    get_response = await client.get(f"/books/{book_id}")
    assert get_response.status_code == 404

# ========== 测试分页排序过滤 ==========

@pytest.mark.asyncio
async def test_books_pagination(client: AsyncClient, auth_headers):
    """测试分页功能"""
    # 创建 5 本书
    for i in range(5):
        book_data = {
            "title": f"图书{i+1}",
            "author": "作者",
            "isbn": f"978000000000{i}",
            "price": 50.00 + i * 10,
        }
        await client.post("/books", json=book_data, headers=auth_headers)
    
    # 测试第 1 页（每页 3 本）
    response = await client.get("/books?page=1&page_size=3")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 3
    assert data["total_pages"] == 2
    assert len(data["items"]) == 3

@pytest.mark.asyncio
async def test_books_sort_by_price(client: AsyncClient, auth_headers):
    """测试按价格排序"""
    # 创建不同价格的书
    prices = [100, 50, 200]
    for i, price in enumerate(prices):
        book_data = {
            "title": f"图书{i}",
            "author": "作者",
            "isbn": f"978111111111{i}",
            "price": price,
        }
        await client.post("/books", json=book_data, headers=auth_headers)
    
    # 按价格降序
    response = await client.get("/books?sort_by=price&order=desc")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    assert items[0]["price"] == 200
    assert items[1]["price"] == 100
    assert items[2]["price"] == 50

@pytest.mark.asyncio
async def test_books_filter_by_author(client: AsyncClient, auth_headers):
    """测试按作者筛选"""
    # 创建不同作者的书
    authors = ["张三", "李四", "王五"]
    for author in authors:
        book_data = {
            "title": f"{author}的书",
            "author": author,
            "isbn": f"97822222222{authors.index(author)}",
            "price": 60.00,
        }
        await client.post("/books", json=book_data, headers=auth_headers)
    
    # 筛选"张三"
    response = await client.get("/books?author=张三")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["author"] == "张三"

@pytest.mark.asyncio
async def test_books_filter_by_price_range(client: AsyncClient, auth_headers):
    """测试价格区间筛选"""
    # 创建不同价格的书
    prices = [30, 50, 80, 120]
    for i, price in enumerate(prices):
        book_data = {
            "title": f"图书{i}",
            "author": "作者",
            "isbn": f"978333333333{i}",
            "price": price,
        }
        await client.post("/books", json=book_data, headers=auth_headers)
    
    # 筛选 50-100 之间
    response = await client.get("/books?min_price=50&max_price=100")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2  # 50 和 80
    for item in data["items"]:
        assert 50 <= item["price"] <= 100
