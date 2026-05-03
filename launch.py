print("[SYSTEM] Starting Assistant...")

try:
    from main import main
    main()
except Exception as e:
    print("[FATAL ERROR]", e)
    print("Run: python main.py for debug mode")
