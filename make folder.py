import os

# exist_ok=True 同樣能防止「資料夾已存在」的錯誤
os.makedirs(r".\sandbox_root\bin", exist_ok=True)
os.makedirs(r".\sandbox_root\Users", exist_ok=True)
os.makedirs(r".\sandbox_root\Users\user1", exist_ok=True)
os.makedirs(r".\sandbox_root\Temp", exist_ok=True)
os.makedirs(r".\sandbox_root\Users\user2", exist_ok=True)
os.makedirs(r".\sandbox_root\Users\user3", exist_ok=True)
