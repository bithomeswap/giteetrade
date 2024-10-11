#include "pch.h"
#include <windows.h>
#include <tlhelp32.h>
#include <iostream>

extern "C" __declspec(dllexport) DWORD_PTR GetDllBaseAddress(DWORD processID, const wchar_t* dllName);
extern "C" __declspec(dllexport) BOOL WriteMemory(DWORD processID, LPCVOID address, ULONG value);
extern "C" __declspec(dllexport) ULONG GetMemory(DWORD processID, LPCVOID address);

DWORD_PTR GetDllBaseAddress(DWORD processID, const wchar_t* dllName) {
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, processID);
    if (hSnapshot == INVALID_HANDLE_VALUE) {
        return NULL;
    }

    MODULEENTRY32W moduleEntry;
    moduleEntry.dwSize = sizeof(MODULEENTRY32W);

    if (Module32FirstW(hSnapshot, &moduleEntry)) {
        do {
            if (wcscmp(moduleEntry.szModule, dllName) == 0) {
                CloseHandle(hSnapshot);
                return (DWORD_PTR)moduleEntry.modBaseAddr;
            }
        } while (Module32NextW(hSnapshot, &moduleEntry));
    }

    CloseHandle(hSnapshot);
    return NULL;
}

BOOL WriteMemory(DWORD processID, LPCVOID address, ULONG value) {
    HANDLE process = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processID);
    if (process == NULL) {
        return FALSE;
    }

    SIZE_T bytesWritten;
    BOOL result = WriteProcessMemory(process, (LPVOID)address, &value, sizeof(value), &bytesWritten);

    CloseHandle(process);
    return result;
}

ULONG GetMemory(DWORD processID, LPCVOID address) {
    HANDLE process = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processID);
    if (process == NULL) {
        return 0;
    }

    ULONG data;
    SIZE_T bytesRead;
    BOOL result = ReadProcessMemory(process, (LPCVOID)address, &data, sizeof(data), &bytesRead);

    CloseHandle(process);
    return result ? data : 0;
}
