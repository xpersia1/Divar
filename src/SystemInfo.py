import platform
import subprocess

def get_system_info():
    # تشخیص سیستم عامل و معماری
    system = platform.system()
    arch = platform.machine()
    os_version = platform.mac_ver()[0] if system == "Darwin" else platform.version()

    # دریافت نسخه Chrome نصب‌شده (در مک)
    try:
        chrome_version = subprocess.check_output(
            "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version",
            shell=True,
            text=True
        ).strip().replace("Google Chrome ", "")
    except:
        chrome_version = "126.0.0.0"  # Fallback در صورت خطا

    # ساخت User Agent
    if system == "Darwin":
        # برای مک‌های Apple Silicon (مانند M1/M2) یا Intel
        if "arm" in arch.lower():
            hardware_model = "Macintosh; Apple M1"
        else:
            hardware_model = "Macintosh; Intel Mac OS X {}".format(os_version.replace(".", "_"))

        user_agent = (
            f"Mozilla/5.0 ({hardware_model}) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{chrome_version} Safari/537.36"
        )
    else:
        user_agent = (
            f"Mozilla/5.0 ({system}; {arch}) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{chrome_version} Safari/537.36"
        )

    return user_agent

if __name__ == "__main__":
    user_agent = get_system_info()
    print("User Agent سیستم شما:")
    print(user_agent)
    print("\nمی‌توانید این مقدار را در Selenium استفاده کنید:")
    print(f'chrome_options.add_argument("user-agent={user_agent}")')