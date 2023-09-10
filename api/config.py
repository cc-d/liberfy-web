# api/config.py
DATABASE_URL = "postgresql+asyncpg://pguser@localhost:5432/libaidb"
JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Change this!
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_SECS = 60 * 60 * 2  # 2 hours
HOST = "localhost"
PORT = 8888
