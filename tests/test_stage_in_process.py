import re

import pytest
from playwright.sync_api import Page, expect



@pytest.mark.skip
def test_authorization_stage(page: Page):
    page.goto("https://re.sr.inventive.ru/")
    profile_icon = page.locator(".header-icons__lk")
    profile_icon.click()
    auth_button = page.get_by_role("button", name="Войти или зарегистрироваться")
    auth_button.click()
    modal = page.locator(".modal-box-auth")
    expect(modal).to_be_visible(timeout=5000)
    heading = modal.locator(".form-auth__heading")
    expect(heading).to_be_visible()
    expect(heading).to_have_text("Вход или регистрация")

    # ====== Проверяем кнопки переключения ======
    # Кнопка "Войти по номеру телефона"
    phone_tab = modal.get_by_role("button", name="Войти по номеру телефона")
    expect(phone_tab).to_be_visible()
    expect(phone_tab).to_be_enabled()

    # Кнопка "Войти по почте"
    email_tab = modal.get_by_role("button", name="Войти по почте")
    expect(email_tab).to_be_visible()
    expect(email_tab).to_be_enabled()

    # ====== Проверяем Яндекс авторизацию ======
    yandex_auth = modal.locator(".yandex-auth")
    expect(yandex_auth).to_be_visible()

    # Проверяем iframe Яндекс
    yandex_iframe = yandex_auth.locator("iframe")
    expect(yandex_iframe).to_be_visible()

    # ====== Проверяем текст с политикой ======
    policy_text = modal.locator(".text-helper")
    expect(policy_text).to_contain_text("Нажимая кнопку “Войти”")
    expect(policy_text).to_contain_text("политики обработки персональных данных")
    expect(policy_text).to_contain_text("политикой конфиденциальности")
    expect(policy_text).to_contain_text("условиями оферты")

    # ====== Проверяем ссылки ======
    # Ссылка на политику обработки данных
    policy_link = modal.get_by_role("link", name="политики обработки персональных данных")
    expect(policy_link).to_be_visible()
    expect(policy_link).to_have_attribute("href",
                                          "https://static.re-store.ru/upload/obrabotka-personalnyh-dannyh-resell.pdf")
    expect(policy_link).to_have_attribute("target", "_blank")

    # Ссылка на политику конфиденциальности
    privacy_link = modal.get_by_role("link", name="политикой конфиденциальности")
    expect(privacy_link).to_be_visible()
    expect(privacy_link).to_have_attribute("href", "/oferta/politika/")

    # Ссылка на оферту
    offer_link = modal.get_by_role("link", name="условиями оферты")
    expect(offer_link).to_be_visible()
    expect(offer_link).to_have_attribute("href", "/oferta/")

    # ====== Проверяем QR код ======
    qr_block = modal.locator(".form-auth__qr")
    expect(qr_block).to_be_visible()

    qr_text = qr_block.locator(".form-auth__qr-text")
    expect(qr_text).to_contain_text("В приложении удобнее!")
    expect(qr_text).to_contain_text("Скачайте мобильное приложение restore")

    qr_image = qr_block.locator(".form-auth__qr-img svg")
    expect(qr_image).to_be_visible()

    print("✅ Все элементы модального окна проверены")
    phone_tab.click()

    phone_input = modal.locator('input[type="tel"]')
    expect(phone_input).to_be_visible()

    test_phone = "79870971700"
    phone_input.fill(test_phone)
    expect(phone_input).to_have_value('+7 (987) 097-17-00')

    with page.expect_response(
            lambda response: "flash-call" in response.url or "code/phone" in response.url
    ) as response_info:
        page.get_by_role("button", name="Войти", exact=True).click()

    # Получаем ответ
    response = response_info.value
    assert response.status == 200, f"Статус: {response.status}"

    # Парсим JSON
    response_data = response.json()
    print(f"Ответ: {response_data}")

    # Извлекаем код с проверкой
    code = None

    # Проверяем, что response_data - словарь
    if isinstance(response_data, dict):
        # Ищем код
        if "debug" in response_data and isinstance(response_data["debug"], dict):
            if "sendResult" in response_data["debug"] and isinstance(response_data["debug"]["sendResult"], dict):
                code = response_data["debug"]["sendResult"].get("code")

    # Если код не найден - ошибка
    assert code is not None, f"Код не найден в ответе: {response_data}"

    code = str(code)
    print(f"✅ Код: {code}")

    # Ждем поля для ввода
    code_modal = page.locator(".form-code-sms")
    expect(code_modal).to_be_visible(timeout=10000)

    # Вводим код
    fields = code_modal.locator('.code__field input[type="number"]')
    for i, digit in enumerate(code):
        fields.nth(i).fill(digit)
        page.wait_for_timeout(100)

    # Ждем результат
    expect(page.locator(".modal-box-auth")).not_to_be_visible(timeout=10000)
    print("✅ Авторизация успешна!")


@pytest.mark.skip
def test_check_stage_catalog(page: Page):
    page.goto("https://re.sr.inventive.ru//naushniki/brand_apple/")

    # 1. Карточки товаров
    product_cards = page.locator("div.catalog__products div.catalog__product-card-hovered")
    last_product = page.locator("xpath=/html/body/main/div[2]/div[2]/div/div[2]/div[1]/div/div/div[1]/div[26]")

    expect(last_product).to_be_visible()


    # 2. Кнопка "Показать еще"
    show_more_btn = page.locator(
         "button.btn.btn--black.btn--size-sm.btn--full-width",
            has_text="Показать еще"
    )
    expect(show_more_btn).to_be_visible()

    # 3. Текст пагинации "Вы посмотрели 24 из 109 товаров"
    pagination_info = page.locator("div.pagination__info")

    expect(pagination_info).to_be_visible()

    text = pagination_info.inner_text()

    # проверяем фиксированную часть + парсим общее число
    match = re.search(r"Вы посмотрели\s+24\s+из\s+(\d+)\s+товаров", text)

    assert match is not None, f"Unexpected pagination text: {text}"

    total_products = int(match.group(1))
    assert total_products > 24
