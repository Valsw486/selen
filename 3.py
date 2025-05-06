from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def main():
    # Настройка веб-драйвера для Firefox
    driver = webdriver.Firefox()

    print("Добро пожаловать в Википедию!")

    while True:
        query = input("Введите ваш запрос (или 'выход' для завершения): ")
        if query.lower() == 'выход':
            break

        # Переход к странице Википедии по запросу
        driver.get(f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}")

        # Получаем заголовок статьи
        title = driver.find_element(By.ID, "firstHeading").text
        print(f"\nВы находитесь на странице: {title}")

        while True:
            # Листаем параграфы статьи
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
            for i, paragraph in enumerate(paragraphs):
                print(f"{i + 1}. {paragraph.text.strip()}\n")

            print("\nВыберите действие:")
            print("1. Листать параграфы статьи.")
            print("2. Перейти на одну из связанных страниц.")
            print("3. Выйти из программы.")

            action = input("Введите номер действия: ")

            if action == '1':
                # Просто продолжаем показывать  параграфы
                continue

            elif action == '2':
                # Получаем связанные ссылки
                related_links = driver.find_elements(By.XPATH, "//a[@href and not(contains(@href, ':'))]")
                print("\nСвязанные страницы:")
                for i, link in enumerate(related_links[:5]):  # Показываем первые 5 связанных ссылок
                    title = link.get_attribute('title')
                    href = link.get_attribute('href')
                    print(f"{i + 1}. {title} ({href})")

                link_choice = input("Введите номер страницы, чтобы перейти (или 'назад' для возврата): ")
                if link_choice.lower() == 'назад':
                    break
                try:
                    index = int(link_choice) - 1
                    if 0 <= index < len(related_links):
                        related_page = related_links[index].get_attribute('href')
                        driver.get(related_page)
                        break
                except (ValueError, IndexError):
                    print("Неверный выбор. Попробуйте снова.")

            elif action == '3':
                print("Выход из программы.")
                driver.quit()
                return

            else:
                print("Неверный выбор. Попробуйте снова.")

            if __name__ == "__main__":
                main()