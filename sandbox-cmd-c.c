#include <windows.h>
#include <stdio.h>
#include <sddl.h>
#include <stdlib.h>
#include <locale.h>

char* utf16_to_utf8(const wchar_t* utf16_str) {
    if (utf16_str == NULL) return NULL;

    // 1. 計算轉換後需要的位元組數 (包含 null 終止符)
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, utf16_str, -1, NULL, 0, NULL, NULL);
    
    // 2. 分配空間
    char* utf8_str = (char*)malloc(size_needed);
    
    // 3. 執行轉換
    WideCharToMultiByte(CP_UTF8, 0, utf16_str, -1, utf8_str, size_needed, NULL, NULL);
    
    return utf8_str;
}

wchar_t* CharToWChar(const char* charArray) {
    // 1. 計算轉換後需要的寬字元長度 (包含結尾 \0)
    int wlen = MultiByteToWideChar(CP_UTF8, 0, charArray, -1, NULL, 0);
    
    // 2. 配置記憶體
    wchar_t* wArray = (wchar_t*)malloc(wlen * sizeof(wchar_t));
    
    // 3. 真正進行轉換
    MultiByteToWideChar(CP_UTF8, 0, charArray, -1, wArray, wlen);
    
    return wArray;
}

char *read(char *file){
    FILE *fp;
    char* buffer = (char*)malloc(3096 * sizeof(char));
    /*
    char buffer[3096]
    C:\Users\原神\Desktop\10011>gcc windows.c -o windows
windows.c: In function 'read':
windows.c:35:12: warning: function returns address of local variable [-Wreturn-local-addr]
     return buffer;
            ^~~~~~
    char *buffer;
    buffer -> 中文亂碼
    */
    // 開啟檔案 (r 代表 read)
    fp = fopen(file, "r"); 
    if (fp == NULL) {
        printf("開啟檔案失敗");
        return NULL;
    }
    
    // 逐行讀取直到結尾
    fgets(buffer, 3096, fp);
    
    fclose(fp);
    
    return buffer;
}

char* LPWSTR_to_UTF8(LPWSTR w_str) {
    if (w_str == NULL) return NULL;

    // 正確使用 WideCharToMultiByte：將「寬字元」轉為「多位元組」
    // 1. 取得所需的 buffer 大小
    int size_needed = WideCharToMultiByte(CP_UTF8, 0, w_str, -1, NULL, 0, NULL, NULL);
    
    char* utf8_str = (char*)malloc(size_needed);

    // 2. 執行轉換
    WideCharToMultiByte(CP_UTF8, 0, w_str, -1, utf8_str, size_needed, NULL, NULL);

    return utf8_str;
}

int main(int argc, char *WTF_this_argv[]) {
    
    char name[1024];
    
    SetConsoleCP(CP_UTF8);// 1. Set the console input code page to UTF-8 (65001)
    setlocale(LC_ALL, ".UTF8"); // 或 ".65001"
    SetConsoleOutputCP(CP_UTF8); // 設定輸出編碼為 UTF-8
    
    LPWSTR *w_argv = CommandLineToArgvW(GetCommandLineW(), &argc);
    
    wchar_t* commands;
    
    if(argc<2){
        printf("pls give commands:");
        //return 1;
        //printf("Enter your full name: ");
        // Syntax: fgets(buffer, size, input_stream)
        fgets(name, sizeof(name), stdin);
        char n1[1024];       
        sprintf(n1,"\"C:\\Windows\\System32\\cmd.exe\" /v /c \"%s\"",name);
        //printf("%s",n1);
        commands = CharToWChar(n1);
    }
    else{
        char* y = LPWSTR_to_UTF8(w_argv[1]);
        char n1[1024];       
        sprintf(n1,"\"C:\\Windows\\System32\\cmd.exe\" /v /c \"%s\"",y);
        commands = CharToWChar(n1);
        //sprintf(name, "%s", argv[1]);
    }
    
    HANDLE hToken = NULL;
    HANDLE hNewToken = NULL;
    PROCESS_INFORMATION pi = {0};
    STARTUPINFOW si = {sizeof(si)};
    
    // 1. 取得目前處理序的存取權杖
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ALL_ACCESS, &hToken)) {
        printf("無法取得 Token: %d\n", GetLastError());
        return 1;
    }
    
    // 2. 建立受限權杖 (閹割管理員權限)
    if (!CreateRestrictedToken(hToken, DISABLE_MAX_PRIVILEGE, 0, NULL, 0, NULL, 0, NULL, &hNewToken)) {
        printf("建立受限 Token 失敗: %d\n", GetLastError());
        CloseHandle(hToken);
        return 1;
    }
    
    // 3. 設定低完整性層級 (防止寫入桌面/系統資料夾)
    TOKEN_MANDATORY_LABEL tml = {0};
    BYTE sid[SECURITY_MAX_SID_SIZE];
    DWORD sidLen = SECURITY_MAX_SID_SIZE;
    CreateWellKnownSid(WinLowLabelSid, NULL, sid, &sidLen);
    tml.Label.Attributes = SE_GROUP_INTEGRITY;
    tml.Label.Sid = (PSID)sid;
    
    if (!SetTokenInformation(hNewToken, TokenIntegrityLevel, &tml, sizeof(tml))) {
        printf("設定完整性層級失敗: %d\n", GetLastError());
    }
    
    // 4. 準備隔離的環境變數 (Environment Block)
    // 這裡手動構造環境變數，最後必須以兩個 \0 結尾
    // 注意：這裡我將 PATH 指向你 Python 腳本搬運後的 sandbox_root\bin
    /* WCHAR lpEnv[] = 
        L"PATH=C:\\sandbox_root\\bin;C:\\Windows\\system32\0"
        L"SYSTEMROOT=C:\\Windows\0"
        L"USERPROFILE=C:\\sandbox_root\\Home\0"
        L"TEMP=C:\\sandbox_root\\Temp\0"
        L"\0"; 
    */
    // 5. 取得目前路徑 (明確使用 W 版本)
    WCHAR currentDir[MAX_PATH];
    GetCurrentDirectoryW(MAX_PATH, currentDir);
    
    printf("正在啟動硬性隔離 CLI (類新 Windows 環境)...\n");
    printf("當前鎖定目錄");
    wprintf(L"當前鎖定目錄: %ls\n", currentDir);
    //!!!!after set local utf8, wprint will failed on uf8 output 
    
    //wchar_t commands[] = L"C:\\Windows\\System32\\cmd.exe";
    //char cmd[] = "\"C:\\Windows\\System32\\cmd.exe\"  /k \"python rw.py\"";
    
    /*
    printf("0 %s",buffer);
    */
    //return 0;
    /*
    char cmd[3096];
    
    sprintf(cmd, "%s", buffer);
    
    printf("1 %s",cmd);
    */
    //char* buffer = read(argv[1]);
    //char* buffer = name;
    //printf(buffer);
    /*
    char* y = LPWSTR_to_UTF8(w_argv[1]);
    wchar_t* commands = CharToWChar(y);
    printf("3 %ls\n",commands);
    */
    /*
    printf("2");
    
    wprintf(L"3 %ls",commands);
    */
    //return 0;
    // 6. 啟動進程 (明確使用 W 版本)
    // 增加 CREATE_UNICODE_ENVIRONMENT 標記，因為我們用了寬字元環境塊
    /*
    BOOL success = CreateProcessAsUserW(
        hNewToken,            // 1. 使用者 Token
        NULL,                 // 2. 執行檔路徑 (建議傳 NULL)
        command,              // 3. 指令與參數 (必須是可寫入的 wchar_t 陣列)
        NULL,                 // 4. 進程安全屬性
        NULL,                 // 5. 執行緒安全屬性
        FALSE,                // 6. 是否繼承控制代碼
        CREATE_NEW_CONSOLE | CREATE_UNICODE_ENVIRONMENT, // 7. 建立旗標
        NULL,                 // 8. 環境變數塊 (若有 CreateEnvironmentBlock 則放這)
        currentDir,           // 9. 工作目錄
        &si,                  // 10. STARTUPINFOW 結構指標
        &pi                   // 11. PROCESS_INFORMATION 結構指標
    );
    */
    if  (CreateProcessAsUserW
            (
                hNewToken, 
                NULL,
                commands, 
                NULL, 
                NULL, 
                FALSE, 
                CREATE_NEW_CONSOLE | CREATE_UNICODE_ENVIRONMENT, 
                NULL,
                currentDir, 
                &si, 
                &pi
            )
        ) 
    {
        printf("啟動成功！此視窗現在是低權限且擁有隔離的 PATH。\n");
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    } else {
        printf("啟動失敗 (ErrorCode): %d\n", GetLastError());
    }
    
    CloseHandle(hNewToken);
    CloseHandle(hToken);
    return 0;
}