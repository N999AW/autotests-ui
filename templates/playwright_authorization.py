from playwright.sync_api import sync_playwright, expect  # Импорт Playwright для синхронного режима и проверки

# Запуск Playwright в синхронном режиме
with sync_playwright() as playwright:
    # Открываем браузер Chromium (не в headless режиме, чтобы видеть действия)
    browser = playwright.firefox.launch(headless=False)
    page = browser.new_page()  # Создаем новую страницу

    # Переходим на страницу авторизации
    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")

    # Находим поле "Email" и заполняем его
    email_input = page.get_by_test_id('login-form-email-input').locator('input')
    email_input.fill("user.name@gmail.com")

    # Находим поле "Password" и заполняем его
    password_input = page.get_by_test_id('login-form-password-input').locator('input')
    password_input.fill("password")

    # Находим кнопку "Login" и кликаем на нее
    login_button = page.get_by_test_id('login-page-login-button')
    login_button.click()

    # Проверяем, что появилось сообщение об ошибке
    wrong_email_or_password_alert = page.get_by_test_id('login-page-wrong-email-or-password-alert')
    expect(wrong_email_or_password_alert).to_be_visible()  # Проверяем видимость элемента
    expect(wrong_email_or_password_alert).to_have_text("Wrong email or password")  # Проверяем текст

    # Пауза на 5 секунд, чтобы увидеть результат
    page.wait_for_timeout(5000)