import os
import shutil
from pathlib import Path

def copy_all(src, dst):
    for root, dirs, files in os.walk(src):
        # 1. Get the relative path from the source root
        rel_path = os.path.relpath(root, src)
        
        # 2. Create corresponding directory in the destination
        dest_dir = os.path.join(dst, rel_path)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except Exception as e:
               print("mk2",e)
        
        # 3. Copy each file in the current directory
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_dir, file)
            try:
                shutil.copy2(src_file, dst_file)
            except Exception as e:
                print("cy2",e)

def setup_portable_env(target_base="./sandbox_root"):
    # 1. 建立沙盒根目錄
    bin_dir = Path(target_base) / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    new_paths = [str(bin_dir.absolute())]
    
    print(f"[*] 開始掃描並搬運環境變數中的工具...")
    
    # 3. 掃描系統 PATH
    old_paths = os.environ.get("PATH", "").split(os.pathsep)
    
    for p in old_paths:
        p_path = Path(p)
        if not p_path.exists():
            continue
        d = str(p_path).replace(os.sep,"_").replace(":","_")
        if "C__WINDOWS" in d or "C__ProgramData"==d or "sdp" in d: 
            continue
        d = bin_dir/d
        #print(d,Path(target_base),p_path,str(d))
        #input()
        print(d)
        try:
            shutil.rmtree(d)
        except Exception as e:
            print("rm",e)   
        
        try:
            copy_all(p_path,d)
        except Exception as e:
            print("cy",e) 

    # 4. 產出給 C 語言使用的環境變數格式
    # Windows 的環境塊是以 \0 結尾的字串序列，最後再一個 \0
    print("-" * 30)
    print("[*] 建議的新環境變數設定：")
    fake_env = {
        "PATH": str(bin_dir.absolute()),
        "USERPROFILE": str(Path(target_base).absolute() / "Home"),
        "TEMP": str(Path(target_base).absolute() / "Temp"),
        "PYTHONPATH": str(Path(target_base).absolute())
    }
    
    for k, v in fake_env.items():
        print(f"{k}={v}")
        
    return fake_env

if __name__ == "__main__":
    setup_portable_env()

"""
PS C:\Users\原神\Desktop\10011> python a.py
[*] 開始掃描並搬運環境變數中的工具...
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v10.0_bin
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v10.0_libnvvp
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.2_bin
rm [WinError 5] Access is denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.2_bin\\compute-sanitizer.bat'
cy2 [Errno 13] Permission denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.2_bin\\.\\compute-sanitizer.bat'
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.2_libnvvp
sandbox_root\bin\C__Program Files_Python313_Scripts
sandbox_root\bin\C__Program Files_Python313
sandbox_root\bin\C__Program Files_mingw64_bin
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v12.1_bin
rm [WinError 5] Access is denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v12.1_bin\\compute-sanitizer.bat'
cy2 [Errno 13] Permission denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v12.1_bin\\.\\compute-sanitizer.bat'
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v12.1_libnvvp
sandbox_root\bin\C__Program Files (x86)_NVIDIA Corporation_PhysX_Common
sandbox_root\bin\C__Program Files_NVIDIA Corporation_Nsight Compute 2023.1.0
sandbox_root\bin\C__Program Files_NVIDIA Corporation_NVIDIA NvDLISR
sandbox_root\bin\C__Program Files_ffmpeg-master-latest-win64-gpl_bin
sandbox_root\bin\C__Program Files_dotnet
sandbox_root\bin\C__ProgramData_chocolatey_bin
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v13.0_bin
sandbox_root\bin\C__ProgramData_miniforge3_condabin
sandbox_root\bin\C__Program Files_Git_bin
sandbox_root\bin\C__Program Files (x86)_Microsoft Visual Studio_2022_BuildTools_VC_Redist_MSVC_14.44.35112
sandbox_root\bin\C__Program Files (x86)_Microsoft Visual Studio_2022_BuildTools_VC_Tools_MSVC_14.44.35207_bin_Hostx86_x86
sandbox_root\bin\C__Users_原神_.cargo_bin
sandbox_root\bin\C__Program Files_Docker_Docker_resources_bin
sandbox_root\bin\C__Program Files_nodejs
sandbox_root\bin\C__Program Files_MiKTeX_miktex_bin_x64
sandbox_root\bin\C__Users_原神_.local_bin
sandbox_root\bin\C__Users_原神_AppData_Local_pnpm
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.2_bin
rm [WinError 5] Access is denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.2_bin\\compute-sanitizer.bat'
cy2 [Errno 13] Permission denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.2_bin\\.\\compute-sanitizer.bat'
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.2_libnvvp
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.0_bin
rm [WinError 5] Access is denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.0_bin\\compute-sanitizer.bat'
cy2 [Errno 13] Permission denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.0_bin\\.\\compute-sanitizer.bat'
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v11.0_libnvvp
sandbox_root\bin\C__Program Files_Python313_Scripts
sandbox_root\bin\C__Program Files_Python313
sandbox_root\bin\C__Program Files_mingw64_bin
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v12.1_bin
rm [WinError 5] Access is denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v12.1_bin\\compute-sanitizer.bat'
cy2 [Errno 13] Permission denied: 'sandbox_root\\bin\\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v12.1_bin\\.\\compute-sanitizer.bat'
sandbox_root\bin\C__Program Files_NVIDIA GPU Computing Toolkit_CUDA_v12.1_libnvvp
sandbox_root\bin\C__Program Files (x86)_NVIDIA Corporation_PhysX_Common
sandbox_root\bin\C__Program Files_NVIDIA Corporation_Nsight Compute 2023.1.0
sandbox_root\bin\C__Program Files_NVIDIA Corporation_NVIDIA NvDLISR
sandbox_root\bin\C__Program Files_ffmpeg-master-latest-win64-gpl_bin
sandbox_root\bin\C__Program Files_dotnet
sandbox_root\bin\C__ProgramData_chocolatey_bin
sandbox_root\bin\C__Users_原神_AppData_Local_Microsoft_WindowsApps
rm [WinError 2] The system cannot find the file specified: 'sandbox_root\\bin\\C__Users_原神_AppData_Local_Microsoft_WindowsApps'
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
cy2 [WinError 1920] The file cannot be accessed by the system
------------------------------
[*] 建議的新環境變數設定：
PATH=C:\Users\原神\Desktop\10011\sandbox_root\bin
USERPROFILE=C:\Users\原神\Desktop\10011\sandbox_root\Home
TEMP=C:\Users\原神\Desktop\10011\sandbox_root\Temp
PYTHONPATH=C:\Users\原神\Desktop\10011\sandbox_root
"""

"""
[*] 建議的新環境變數設定：
PATH=.\sandbox_root\bin
USERPROFILE=.\sandbox_root\Users\user1
TEMP=.\sandbox_root\Temp
"""