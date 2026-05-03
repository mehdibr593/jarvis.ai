print("[ASSISTANT] Booting Desktop AI...")

try:
    from main import main
    main()
except Exception as e:
    print("[ERROR]", e)
    print("Fallback: run 'python main.py' for debug mode")
