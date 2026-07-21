import httpx
import asyncio
import time

# 测试同步版本
def test_sync(num_requests=50):
    url = "http://localhost:8000/books"
    start = time.time()
    
    with httpx.Client() as client:
        for _ in range(num_requests):
            response = client.get(url)
    
    duration = time.time() - start
    print(f"同步版本：{num_requests} 个请求耗时 {duration:.2f} 秒")
    return duration

# 测试异步版本
async def test_async(num_requests=50):
    url = "http://localhost:8001/books"
    start = time.time()
    
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for _ in range(num_requests)]
        await asyncio.gather(*tasks)
    
    duration = time.time() - start
    print(f"异步版本：{num_requests} 个请求耗时 {duration:.2f} 秒")
    return duration

# 运行对比测试
if __name__ == "__main__":
    print("🚀 开始性能测试...\n")
    
    sync_time = test_sync(50)
    async_time = asyncio.run(test_async(50))
    
    speedup = sync_time / async_time
    print(f"\n📊 结果：异步版本快了 {speedup:.2f} 倍！")