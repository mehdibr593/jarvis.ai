print("[Jarvis AI] Starting...")

try:
    from main import main
    main()
except Exception as e:
    print("[ERROR]", e)
    print("Fallback: running main.py")
    import os
    os.system("python3 main.py")
