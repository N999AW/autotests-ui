
import pytest
from playwright.sync_api import Page, expect

def check_header(page: Page, url: str):
    """Вспомогательная функция: проверяет хедер на переданной странице"""
    try:
        header_top = page.locator(".header__top")
        assert header_top.count() > 0, f"Блок header__top не найден на {url}"
        assert header_top.is_visible(), f"Блок header__top скрыт на {url}"

        # Дополнительные проверки (опционально)
        location_btn = page.locator(".header__top .location")
        assert location_btn.is_visible(), f"Кнопка локации не видна на {url}"

        # Проверяем, что есть хотя бы 3 ссылки в сервисном меню
        service_links = page.locator(".header-services__row a")
        assert service_links.count() >= 3, f"Меню услуг содержит мало ссылок на {url}"

        print(f"  ✅ Хедер на {url} в порядке")
        return True
    except Exception as e:
        print(f"  ❌ Ошибка хедера на {url}: {e}")
        return False


def test_check_stage_categories(page: Page):
    """Проверка: На всех страницах категорий есть ожидаемые подкатегории И хедер"""
    data = {
        "https://re.sr.inventive.ru/apple/": [
            "iPhone",
            "Mac",
            "Watch",
            "iPad",
            "AirPods",
            "Аксессуары Apple",
        ],
        "https://re.sr.inventive.ru/smartfony-i-gadzhety/": [
            "Смартфоны",
            "Планшеты",
            "Умные часы",
            "Фитнес-браслеты",
            "Наушники",
            "Игры и консоли",
            "Портативная акустика",
            "Умный дом",
            "Samsung",
            "HUAWEI",
            "Xiaomi",
        ],
        "https://re.sr.inventive.ru/kompyutery-i-noutbuki/": [
            "Ноутбуки",
            "Моноблоки",
            "Системные блоки и мини-ПК",
            "Мониторы",
            "Планшеты",
            "Сетевое оборудование",
            "Клавиатуры, мышки, стилусы",
        ],
        "https://re.sr.inventive.ru/tv-audio-video/": [
            "Телевизоры, проекторы, экраны",
            "Hi-Fi и акустика",
            "Наушники",
            "Видеокамеры и съемка",
            "Звук",
        ],
        "https://re.sr.inventive.ru/dlya-doma/": [
            "Бытовая техника",
            "ТВ, видео-аудио",
            "Умный дом",
            "Гейминг",
            "Для кухни",
            "Освещение",
            "Товары для питомцев",
            "Интерьер",
            "Мебель",
            "Для ванной",
            "Инструменты",
        ],
        "https://re.sr.inventive.ru/krasota-i-zdorove/": [
            "Укладка и уход за волосами",
            "Уход за лицом и телом",
            "Уход за полостью рта",
            "Умные весы",
            "Датчики и трекеры",
            "Тренажеры",
            "Фитнес-браслеты",
        ],
        "https://re.sr.inventive.ru/razvlecheniya/": [
            "Гейминг",
            "Дроны",
            "Роботы и игрушки",
            "Обучение",
            "Принтеры и печать",
            "Тренажеры",
            "Звук",
            "Книги",
        ],
        "https://re.sr.inventive.ru/puteshestviya-i-sport/": [
            "Сумки и рюкзаки",
            "Умные бутылки",
            "Умные часы и фитнес-трекеры",
            "Экшн-камеры",
            "Тренажеры",
            "Очки для спорта",
            "Умные очки",
            "Умные кольца",
        ],
        "https://re.sr.inventive.ru/aksessuary/": [
            "Чехлы и защита",
            "Ремешки",
            "Клавиатуры, мышки, стилусы",
            "Питание и кабели",
            "Накопители",
            "Сумки и рюкзаки",
            "Держатели для устройств",
            "Сетевое оборудование",
            "Поисковые трекеры",
            "Чистящие средства",
        ],
    }

    errors = []
    header_errors = []

    for url, categories in data.items():
        print(f"\n🔍 Проверяем страницу: {url}")
        page.goto(url)

        # ====== ПРОВЕРКА 1: Хедер на этой странице ======
        if not check_header(page, url):
            header_errors.append(f"{url} -> ❌ Проблемы с хедером")

        # ====== ПРОВЕРКА 2: Категории на этой странице ======
        for category in categories:
            locator = page.locator(f'.card__title:text-is("{category}")')

            try:
                expect(locator).to_have_count(1, timeout=3000)
                expect(locator).to_be_visible(timeout=3000)
                print(f"  ✅ {category}")
            except Exception:
                errors.append(f"{url} -> ❌ {category}")
                print(f"  ❌ {category} (НЕ НАЙДЕНА)")

    # Выводим итоговый отчет
    print("\n" + "=" * 50)
    print("📊 ИТОГОВЫЙ ОТЧЕТ:")

    if header_errors:
        print("\n🔴 ПРОБЛЕМЫ С ХЕДЕРОМ:")
        for err in header_errors:
            print(f"  {err}")
    else:
        print("  ✅ Хедер работает на всех страницах")

    if errors:
        print("\n🔴 ПРОБЛЕМЫ С КАТЕГОРИЯМИ:")
        for err in errors:
            print(f"  {err}")
    else:
        print("  ✅ Все категории найдены")

    print("=" * 50)

    # Если есть ошибки — тест падает
    all_errors = errors + header_errors
    assert not all_errors, "\n".join(all_errors)

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestStageAppleCategories():
    def test_check_stage_catalog_apple(self, page: Page):
        """Проверка: Все страницы iPhone открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/smartfony/apple/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-17-pro-max/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-17-pro/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-air/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-17/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-17e/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-16-pro/type_iphone-16-pro-max/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-16-pro/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-16/",
            "https://re.sr.inventive.ru/smartfony/apple/iphone-15/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц iPhone:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все страницы iPhone открываются корректно")

    def test_check_stage_catalog_mac(self, page: Page):
        """Проверка: Все страницы Mac открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/macbook-air/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/macbook-pro/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/macbook-neo/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/mac-mini/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/imac/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/mac-studio/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/type_of_computer_monitory/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Mac:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все страницы Mac открываются корректно")

    def test_check_stage_catalog_watch(self, page: Page):
        """Проверка: Все страницы Watch открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/smart-chasy/apple/",
            "https://re.sr.inventive.ru/smart-chasy/apple/watch-ultra-3/",
            "https://re.sr.inventive.ru/smart-chasy/apple/watch-series-11/",
            "https://re.sr.inventive.ru/smart-chasy/apple/watch-se-3/",
            "https://re.sr.inventive.ru/smart-chasy/apple/watch-ultra-2/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Watch:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все страницы Watch открываются корректно")

    def test_check_stage_catalog_ipad(self, page: Page):
        """Проверка: Все страницы iPad открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/planshety/apple/",
            "https://re.sr.inventive.ru/planshety/apple/ipad-pro/",
            "https://re.sr.inventive.ru/planshety/apple/ipad-air/",
            "https://re.sr.inventive.ru/planshety/apple/ipad/",
            "https://re.sr.inventive.ru/planshety/apple/ipad-mini/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц iPad:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все страницы Watch открываются корректно")

    def test_check_stage_catalog_airpods(self, page: Page):
        """Проверка: Все страницы Airpods открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/naushniki/brand_apple/",
            "https://re.sr.inventive.ru/naushniki/airpods-pro/",
            "https://re.sr.inventive.ru/naushniki/airpods-max/",
            "https://re.sr.inventive.ru/naushniki/airpods-max/type_airpods-max-2/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Airpods:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все страницы Airpods открываются корректно")

    def test_check_stage_catalog_accessories(self, page: Page):
        """Проверка: Все страницы Аксессуаров Apple открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/cases-protectors/cases/brand_apple/",
            "https://re.sr.inventive.ru/input-information/brand_apple/",
            "https://re.sr.inventive.ru/bands/brand_apple/",
            "https://re.sr.inventive.ru/power-cables/brand_apple/",
            "https://re.sr.inventive.ru/trackers/brand_apple/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Аксессуаров:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все страницы Аксессуаров Apple открываются корректно")

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestStageSmartphonesCategories():
    def test_check_stage_catalog_smartphones(self, page: Page):
        """Проверка: Все страницы смартфонов открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/smartfony/",
            "https://re.sr.inventive.ru/smartfony/apple/",
            "https://re.sr.inventive.ru/smartfony/samsung/",
            "https://re.sr.inventive.ru/smartfony/huawei/",
            "https://re.sr.inventive.ru/smartfony/motorola/",
            "https://re.sr.inventive.ru/smartfony/redmi/",
            "https://re.sr.inventive.ru/smartfony/",
            "https://re.sr.inventive.ru/software/arch_smartfony/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц смартфонов:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все смартфоны открываются корректно")

    def test_check_stage_catalog_tablets(self, page: Page):
        """Проверка: Все страницы планшетов открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/planshety/",
            "https://re.sr.inventive.ru/planshety/apple/",
            "https://re.sr.inventive.ru/planshety/samsung/",
            "https://re.sr.inventive.ru/planshety/xiaomi/",
            "https://re.sr.inventive.ru/planshety/huawei/",
            "https://re.sr.inventive.ru/planshety/redmi/",
            "https://re.sr.inventive.ru/planshety/",
            "https://re.sr.inventive.ru/software/arch_planshety/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц планшетов:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все планшеты открываются корректно")

    def test_check_stage_catalog_smartwatch(self, page: Page):
        """Проверка: Все страницы умных часов открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/smart-chasy/",
            "https://re.sr.inventive.ru/smart-chasy/apple/",
            "https://re.sr.inventive.ru/smart-chasy/samsung/",
            "https://re.sr.inventive.ru/smart-chasy/garmin/",
            "https://re.sr.inventive.ru/smart-chasy/xiaomi/",
            "https://re.sr.inventive.ru/smart-chasy/huawei/",
            "https://re.sr.inventive.ru/smart-chasy/watch_type_kids-watch/",
            "https://re.sr.inventive.ru/smart-chasy/",
            "https://re.sr.inventive.ru/bands/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц умных часов:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все умные часы открываются корректно")

    def test_check_stage_catalog_fitness_trackers(self, page: Page):
        """Проверка: Все страницы фитнес-браслетов открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/smart-chasy/watch_type_fitness-bracelet/",
            "https://re.sr.inventive.ru/smart-chasy/whoop/watch_type_fitness-bracelet/",
            "https://re.sr.inventive.ru/smart-chasy/xiaomi/watch_type_fitness-bracelet/",
            "https://re.sr.inventive.ru/smart-chasy/google/watch_type_fitness-bracelet/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц фитнес-браслетов:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все фитнес-браслеты открываются корректно")

    def test_check_stage_catalog_headphones(self, page: Page):
        """Проверка: Все страницы наушников открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/naushniki/",
            "https://re.sr.inventive.ru/naushniki/besprovodnye-naushniki/",
            "https://re.sr.inventive.ru/naushniki/provodnye-naushniki/",
            "https://re.sr.inventive.ru/naushniki/",
            "https://re.sr.inventive.ru/naushniki/detskie-naushniki/",
            "https://re.sr.inventive.ru/aksessuary/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц наушников:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Все наушники открываются корректно")

    def test_check_stage_catalog_games(self, page: Page):
        """Проверка: Все страницы игр и консолей открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/igry-i-konsoli/",
            "https://re.sr.inventive.ru/igry-i-konsoli/igrovye-pristavki/",
            "https://re.sr.inventive.ru/igry-i-konsoli/igry/",
            "https://re.sr.inventive.ru/igry-i-konsoli/gejmpady/",
            "https://re.sr.inventive.ru/igry-i-konsoli/aksessuary-igry-i-konsoli/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц игр и консолей:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Игры и консоли открываются корректно")

    def test_check_stage_catalog_akustika(self, page: Page):
        """Проверка: Все страницы акустики открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/akustika/",
            "https://re.sr.inventive.ru/akustika/portativnaya-akustika/",
            "https://re.sr.inventive.ru/akustika/akustika-s-golosovym-pomoshchnikom/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Акустики:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы акустики открываются корректно")

    def test_check_stage_catalog_smart_home(self, page: Page):
        """Проверка: Все страницы умного дома открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/umnyj-dom/",
            "https://re.sr.inventive.ru/upravlenie-i-datchiki/",
            "https://re.sr.inventive.ru/osveshchenie/",
            "https://re.sr.inventive.ru/bezopasnost/",
            "https://re.sr.inventive.ru/klimat/",
            "https://re.sr.inventive.ru/akustika/akustika-s-golosovym-pomoshchnikom/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц умного дома:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы умного дома открываются корректно")

    def test_check_stage_catalog_samsung(self, page: Page):
        """Проверка: Все страницы samsung открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/selection/samsung/",
            "https://re.sr.inventive.ru/smartfony/samsung/galaxy-s26/",
            "https://re.sr.inventive.ru/smartfony/samsung/galaxy-s26-plus/",
            "https://re.sr.inventive.ru/smartfony/samsung/galaxy-s26-ultra/",
            "https://re.sr.inventive.ru/smartfony/samsung/galaxy-z-fold7/",
            "https://re.sr.inventive.ru/smartfony/samsung/galaxy-z-flip7/",
            "https://re.sr.inventive.ru/smart-chasy/samsung/watch8/",
            "https://re.sr.inventive.ru/smart-chasy/samsung/watch8/type_watch8-classic/",
            "https://re.sr.inventive.ru/smart-chasy/samsung/watch-ultra/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц samsung:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы samsung открываются корректно")

    def test_check_stage_catalog_huawei(self, page: Page):
        """Проверка: Все страницы huawei открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/smartfony/huawei/mate-80-pro/",
            "https://re.sr.inventive.ru/smartfony/huawei/nova-15-pro/",
            "https://re.sr.inventive.ru/smartfony/huawei/mate-x7/",
            "https://re.sr.inventive.ru/smartfony/huawei/pura-80/",
            "https://re.sr.inventive.ru/smartfony/huawei/pura-80-pro/",
            "https://re.sr.inventive.ru/smartfony/huawei/pura-80-ultra/",
            "https://re.sr.inventive.ru/planshety/huawei/type_matepad/",
            "https://re.sr.inventive.ru/smart-chasy/huawei/type_gt-runner-2/",
            "https://re.sr.inventive.ru/smart-chasy/huawei/watch-gt/type_watch-gt-5/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц huawei:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы huawei открываются корректно")

    def test_check_stage_catalog_xiaomi(self, page: Page):
        """Проверка: Все страницы xiaomi открываются без ошибок"""

        urls = [
            "https://re.sr.inventive.ru/smartfony/xiaomi/17/",
            "https://re.sr.inventive.ru/smartfony/xiaomi/15/",
            "https://re.sr.inventive.ru/smartfony/xiaomi/15t/",
            "https://re.sr.inventive.ru/smartfony/xiaomi/mix-flip/",
            "https://re.sr.inventive.ru/smart-chasy/xiaomi/smart-band/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц xiaomi:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы xiaomi открываются корректно")

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestStageComputersAndLaptopsCategories():
    def test_check_stage_catalog_laptops(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/kompyutery-noutbuki/type_of_computer_noutbuki/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/type_of_computer_noutbuki/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/samsung/type_of_computer_noutbuki/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/type_of_computer_noutbuki/",
            "https://re.sr.inventive.ru/software/arch_kompyutery-noutbuki/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц ноутбуков:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы ноутбуков открываются корректно")

    def test_check_stage_catalog_all_in_one_pc(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/imac/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку iMac:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы iMac открываются корректно")

    def test_check_stage_catalog_mini_PC(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/kompyutery-noutbuki/type_of_computer_mini-pc;computers/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/mac-studio/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/apple/mac-mini/",
            "https://re.sr.inventive.ru/kompyutery-noutbuki/restore/",
            "https://re.sr.inventive.ru/software/arch_kompyutery-noutbuki/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц системных блоков и мини-ПК:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы системных блоков и мини-ПК открываются корректно")

    def test_check_stage_catalog_monitors(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/kompyutery-noutbuki/type_of_computer_monitory/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку мониторов:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы мониторов открываются корректно")

    def test_check_stage_catalog_networks(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/networks/",
            "https://re.sr.inventive.ru/networks/routery/",
            "https://re.sr.inventive.ru/networks/marshrutizatory/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц сетевого оборудования:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы сетевого оборудования открываются корректно")

    def test_check_stage_catalog_input_information(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/input-information/",
            "https://re.sr.inventive.ru/input-information/peripherals/",
            "https://re.sr.inventive.ru/input-information/mouse/",
            "https://re.sr.inventive.ru/input-information/trackpads/",
            "https://re.sr.inventive.ru/input-information/styluses/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Клавиатуры, мышки, стилусы:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Клавиатуры, мышки, стилусы открываются корректно")

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestStageTVAudioVideo():
    def test_check_stage_catalog_TV(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/tv/",
            "https://re.sr.inventive.ru/tv/televizory/",
            "https://re.sr.inventive.ru/tv/portativnye-proektory/",
            "https://re.sr.inventive.ru/tv/kronshtejny/",
            "https://re.sr.inventive.ru/tv/ramki-dlya-tv/",
            "https://re.sr.inventive.ru/tv/aksessuary-tv/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Телевизоры, проекторы, экраны:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Телевизоры, проекторы, экраны открываются корректно")

    def test_check_stage_catalog_hifi(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/akustika/",
            "https://re.sr.inventive.ru/akustika/stacionarnaya-akustika/",
            "https://re.sr.inventive.ru/akustika/saundbary/",
            "https://re.sr.inventive.ru/akustika/portativnaya-akustika/",
            "https://re.sr.inventive.ru/akustika/akustika-s-golosovym-pomoshchnikom/",
            "https://re.sr.inventive.ru/proigryvateli/",
            "https://re.sr.inventive.ru/akustika/aksessuary-dlya-akustiki/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Hi-Fi и акустика:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Hi-Fi и акустика открываются корректно")

    def test_check_stage_catalog_cameras(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/videokamery-i-semka/",
            "https://re.sr.inventive.ru/videokamery-i-semka/ehkshn-kamery/",
            "https://re.sr.inventive.ru/videokamery-i-semka/umnye-ochki/",
            "https://re.sr.inventive.ru/videokamery-i-semka/derzhateli/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Видеокамера и съемка:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Видеокамера и съемка открываются корректно")

    def test_check_stage_catalog_vinyl(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/proigryvateli/",
            "https://re.sr.inventive.ru/proigryvateli/vinilovye-proigryvateli/",
            "https://re.sr.inventive.ru/proigryvateli/aksessuary-vinilovye-proigryvateli/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Виниловые проигрыватели:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Виниловые проигрыватели открываются корректно")

    def test_check_stage_catalog_sound(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/zvuk/",
            "https://re.sr.inventive.ru/zvuk/mikrofony/",
            "https://re.sr.inventive.ru/zvuk/mikshernye-pulty/",
            "https://re.sr.inventive.ru/obuchenie/transkribatory-perevodchiki/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Звук:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Звук открываются корректно")

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestStageHome():
    def test_check_stage_household_appliances(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/bytovaya-tekhnika/",
            "https://re.sr.inventive.ru/bytovaya-tekhnika/pylesosy-i-moyshchiki/",
            "https://re.sr.inventive.ru/bytovaya-tekhnika/holodilniki/",
            "https://re.sr.inventive.ru/bytovaya-tekhnika/stiralnye-mashiny/",
            "https://re.sr.inventive.ru/bytovaya-tekhnika/sushilnye-mashiny/",
            "https://re.sr.inventive.ru/bytovaya-tekhnika/mikrovolnovye-pechi/",
            "https://re.sr.inventive.ru/bytovaya-tekhnika/duhovye-shkafy/",
            "https://re.sr.inventive.ru/bytovaya-tekhnika/posudomoechnye-mashiny/",
            "https://re.sr.inventive.ru/klimat/kondicionery/",
            "https://re.sr.inventive.ru/bytovaya-tekhnika/aksessuary-dlya-bytovoi-tekhniki/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц бытовая техника:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы бытовая техника открываются корректно")

    def test_check_stage_gaming(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/kitchen-goods/",
            ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Для кухни:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Для кухни открываются корректно")

    def test_check_stage_osveshenie(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/osveshchenie/",
            "https://re.sr.inventive.ru/osveshchenie/sistemy-osveshcheniya/",
            "https://re.sr.inventive.ru/osveshchenie/svetilniki/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Освещение:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Освещение открываются корректно")

    def test_check_stage_pets(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/tovary-dlya-pitomcev/",
            "https://re.sr.inventive.ru/tovary-dlya-pitomcev/lotki-i-ustraniteli-zapahov/",
            "https://re.sr.inventive.ru/tovary-dlya-pitomcev/miski-poilki-kormushki/",
            "https://re.sr.inventive.ru/trackers/",
            "https://re.sr.inventive.ru/tovary-dlya-pitomcev/gruming/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Для питомцев:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Для питомцев открываются корректно")

    def test_check_stage_interer(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/interer/",
            "https://re.sr.inventive.ru/interer/figurki/",
            "https://re.sr.inventive.ru/interer/gorshki-dlya-rastenij/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Интерьер:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Интерьер открываются корректно")

    def test_check_stage_mebel(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/mebel/",
            "https://re.sr.inventive.ru/mebel/umnye-stoly/",
            "https://re.sr.inventive.ru/mebel/igrovye-stoly/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Мебель:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Мебель открываются корректно")

    def test_check_stage_bathroom(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/dlya-vanny/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц для ванной:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы для ванной открываются корректно")

    def test_check_stage_tools(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/instrumenty/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Инструменты:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Инструменты открываются корректно")

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestStageBeauty():
    def test_check_stage_ukladka_i_uhod(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/ukladka-i-uhod-za-volosami/",
            "https://re.sr.inventive.ru/ukladka-i-uhod-za-volosami/feny/",
            "https://re.sr.inventive.ru/ukladka-i-uhod-za-volosami/stajlery/",
            "https://re.sr.inventive.ru/ukladka-i-uhod-za-volosami/vypryamiteli/",
            "https://re.sr.inventive.ru/ukladka-i-uhod-za-volosami/uhod-za-volosami/",
            "https://re.sr.inventive.ru/ukladka-i-uhod-za-volosami/aksessuary-ukladka-volos/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Укладка и уход за волосами:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Уход за лицом и телом открываются корректно")

    def test_check_stage_uhod_za_licom(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/uhod-za-licom-i-telom/",
            "https://re.sr.inventive.ru/uhod-za-licom-i-telom/maski-dlya-lica/",
            "https://re.sr.inventive.ru/uhod-za-licom-i-telom/massazhery/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Уход за лицом и телом:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Укладка и уход за волосами открываются корректно")

    def test_check_stage_uhod_za_polostyu(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/uhod-za-polostyu-rta/",
            "https://re.sr.inventive.ru/uhod-za-polostyu-rta/ehlektricheskie-zubnye-shchetki/",
            "https://re.sr.inventive.ru/uhod-za-polostyu-rta/irrigatory/",
            "https://re.sr.inventive.ru/uhod-za-polostyu-rta/aksessuary-uhod-za-polostyu-rta/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Уход за полостью рта:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Уход за полостью рта открываются корректно")

    def test_check_stage_vesy(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/umnye-vesy/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц весы:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы весы открываются корректно")

    def test_check_stage_manikur(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/manikyur-pedikyur/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Маникюр, педикюр:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Маникюр, педикюр открываются корректно")

    def test_check_stage_trackers(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/datchiki-i-trekery/",
            "https://re.sr.inventive.ru/datchiki-i-trekery/trekery-sna/",
            "https://re.sr.inventive.ru/datchiki-i-trekery/rings/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Датчики и трекеры:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Датчики и трекеры открываются корректно")

    def test_check_stage_trenazhery(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/trenazhery/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Тренажеры:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Тренажеры открываются корректно")

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestEntertainment():
    def test_check_stage_drony(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/kvadrokoptery-i-drony/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Дроны:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Дроны открываются корректно")

    def test_check_stage_robots(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/robots-toys/",
            "https://re.sr.inventive.ru/robots-toys/roboty/",
            "https://re.sr.inventive.ru/robots-toys/konstruktory/",
            "https://re.sr.inventive.ru/robots-toys/radioupravlyaemye-igrushki/",
            "https://re.sr.inventive.ru/robots-toys/nastolnye-igry/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Роботы и игрушки:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Роботы и игрушки открываются корректно")

    def test_check_stage_learning(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/obuchenie/",
            "https://re.sr.inventive.ru/obuchenie/type-e-book/",
            "https://re.sr.inventive.ru/obuchenie/umnye-bloknoty/",
            "https://re.sr.inventive.ru/obuchenie/transkribatory-perevodchiki/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Обучение:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Обучение открываются корректно")

    def test_check_stage_printers(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/printery-i-pechat/",
            "https://re.sr.inventive.ru/printery-i-pechat/printery/",
            "https://re.sr.inventive.ru/printery-i-pechat/printery/photoprinters/",
            "https://re.sr.inventive.ru/printery-i-pechat/aksessuary-printery/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Принтеры и печать:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Принтеры и печать открываются корректно")

    def test_check_stage_transport(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/printery-i-pechat/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Транспорт:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Транспорт открываются корректно")

    def test_check_stage_books(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/knigi/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Книги:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Книги открываются корректно")

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestTravels():
    def test_check_stage_bags(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/bags/",
            "https://re.sr.inventive.ru/bags/backpacks/",
            "https://re.sr.inventive.ru/bags/bag/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Сумки и рюкзаки:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Сумки и рюкзаки открываются корректно")

    def test_check_stage_smart_bottles(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/umnye-butylki-termokruzhki/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Умные бутылки:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Умные бутылки открываются корректно")

    def test_check_stage_smart_action_cameras(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/videokamery-i-semka/ehkshn-kamery/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Экшн-камеры:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Экшн-камеры открываются корректно")

    def test_check_stage_smart_action_sport_glacces(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/ochki-dlya-sporta/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Очки для спорта:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Очки для спорта открываются корректно")

    def test_check_stage_smart_action_sport_rings(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/datchiki-i-trekery/rings/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Умные кольца:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Умные кольца открываются корректно")

@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestAccessories():
    def test_check_stage_cases_protectors(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/cases-protectors/",
            "https://re.sr.inventive.ru/cases-protectors/cases/",
            "https://re.sr.inventive.ru/cases-protectors/cases-keyboard/",
            "https://re.sr.inventive.ru/cases-protectors/screen-protectors/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Чехлы и защита:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Чехлы и защита открываются корректно")

    def test_check_stage_bands(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/bands/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Ремешки:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Ремешки открываются корректно")

    def test_check_stage_power_cables(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/power-cables/",
            "https://re.sr.inventive.ru/power-cables/chargers/",
            "https://re.sr.inventive.ru/power-cables/power/",
            "https://re.sr.inventive.ru/power-cables/dock/",
            "https://re.sr.inventive.ru/power-cables/cables/",
            "https://re.sr.inventive.ru/power-cables/adapters/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Питание и кабели:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Питание и кабели открываются корректно")

    def test_check_stage_power_storage(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/storage/",
            "https://re.sr.inventive.ru/storage/flash-memory/",
            "https://re.sr.inventive.ru/storage/external-storage/",
            "https://re.sr.inventive.ru/storage/memory-card/"
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Накопители:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Накопители открываются корректно")

    def test_check_stage_power_derjately(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/uderzhivayushchie-ustrojstva/",
            "https://re.sr.inventive.ru/uderzhivayushchie-ustrojstva/stabilizatory/",
            "https://re.sr.inventive.ru/uderzhivayushchie-ustrojstva/car-mounters/",
            "https://re.sr.inventive.ru/uderzhivayushchie-ustrojstva/shnurki/",
            "https://re.sr.inventive.ru/uderzhivayushchie-ustrojstva/stands/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц Удерживающие устройства:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Удерживающие устройства открываются корректно")

    def test_check_stage_search_trackers(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/trackers/",
            "https://re.sr.inventive.ru/trackers/poiskovye-trekery/",
            "https://re.sr.inventive.ru/trackers/trekery-dlya-zhivotnyh/",
            "https://re.sr.inventive.ru/trackers/chekhly-i-breloki-dlya-trekerov/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц поисковые трекеры:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы поисковые трекеры открываются корректно")

    def test_check_stage_others(self, page: Page):

        urls = [
            "https://re.sr.inventive.ru/others/cleaners/",
        ]

        errors = []

        print("\n📱 Проверяем загрузку страниц поисковые Разное:")

        for url in urls:
            try:
                page.goto(url, timeout=10000)

                # Проверяем, что страница загрузилась (ждем появления какого-либо элемента)
                page.wait_for_selector("h1, .product-title, .price, .card", timeout=5000)

                # Проверяем, что нет текста 404
                if page.locator("text=404, text=Страница не найдена").count() > 0:
                    errors.append(f"{url} -> ❌ Страница не найдена (404)")
                else:
                    print(f"  ✅ {url} - загружена")

            except Exception as e:
                errors.append(f"{url} -> ❌ Ошибка загрузки: {e}")
                print(f"  ❌ {url} - ошибка")

        assert not errors, "\n".join(errors)
        print("\n✅ Страницы Разное открываются корректно")
