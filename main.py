import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from form_xml import main_format 
from api_sendler import main as main_api 

API_TOKEN = '7946467083:AAFi14SmZRrsmA5iP3lnSKcJHm8bPmogvpQ'
DOWNLOAD_FOLDER = 'downloads'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

myChat = '1098076988'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@dp.message(F.text == '/start')
async def send_welcome(message: types.Message):

    await message.reply("Привет! Отправь мне файл в формате .xlsx, и я его сохраню.")

@dp.message(F.document)
async def handle_document(message: types.Message):
    file_name = message.document.file_name.lower()

    try:
        file_info = await bot.get_file(message.document.file_id)

        if file_name == "gods.xml":
            await bot.download_file(file_info.file_path, destination=file_name)  # сохраняем в корень
            await message.reply("✅ Файл 'gods.xml' успешно сохранён в корень проекта.")
            logging.info("Файл 'gods.xml' сохранён в корне.")
            await bot.send_message(myChat, f"📦 Обновлён файл товаров: gods.xml")
            return

        elif file_name == "cost.xlsx":
            await bot.download_file(file_info.file_path, destination=file_name)
            await message.reply("✅ Файл 'cost.xlsx' успешно сохранён в корень проекта.")
            logging.info("Файл 'cost.xlsx' сохранён в корне.")
            await bot.send_message(myChat, f"📦 Обновлён файл цен: cost.xlsx")
            return

        elif file_name.endswith('.xlsx'):
            file_path_local = os.path.join(DOWNLOAD_FOLDER, file_name)
            await bot.download_file(file_info.file_path, destination=file_path_local)

            await message.reply(f"Файл '{file_name}' успешно сохранён.")
            await bot.send_message(myChat, f"Файл '{file_name}' успешно сохранён.")
            logging.info(f"Файл '{file_name}' сохранён в '{file_path_local}'")

            name_without_extension = file_name[:file_name.rfind('.')]
            xml_file_name = f"{name_without_extension}.xml"

            main_format(file_path_local, xml_file_name)
            main_api(xml_file_name)

            await message.reply(f"Файл '{file_name}' успешно обработан.")
            return

        else:
            await message.reply("❌ Неподдерживаемый формат. Отправьте файл .xlsx или gods.xml.")
            return

    except Exception as e:
        logging.error(f"Ошибка при обработке файла '{file_name}': {e}", exc_info=True)
        await message.reply("❌ Произошла ошибка при обработке файла.")
        await bot.send_message(myChat, f"❌ Ошибка при обработке файла '{file_name}': {e}")


async def hourly_task():

    logging.info("Начинаем задачу по обработке файлов 'Люстдорфська'.")
    current_time_plus_3 = (datetime.now() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M:%S")
    
    processed_files_count = 0
    
    try:
        for file_name in os.listdir(DOWNLOAD_FOLDER):
            if file_name.endswith('.xlsx') and "Люстдорфська".lower() in file_name.lower():
                file_path_local = os.path.join(DOWNLOAD_FOLDER, file_name)
                
                xml_file_name = "Люстдорфська.xml"
                
                try:
                    print(f"Обработка файла: {file_name}")
                    main_format(file_path_local, xml_file_name)
                    print(f"Файл '{file_name}' преобразован в '{xml_file_name}'.")

                    main_api(xml_file_name) 
                    print(f"Файл '{xml_file_name}' отправлен через API.")
                    
                    processed_files_count += 1
                    
                    notification_text = (
                        f"Задача по 'Люстдорфська' завершена. Время: {current_time_plus_3}\n"
                        f"Обработано файлов: {processed_files_count}\n"
                        f"Файл: {file_name}"
                    )

                except Exception as e:
                    print(f"Ошибка при обработке файла '{file_name}' в задаче: {e}", exc_info=True)
                    await bot.send_message(myChat, f"Ошибка при обработке '{file_name}': {e}")
        
        
        await bot.send_message(myChat, notification_text)
        logging.info(notification_text)

    except Exception as e:
        logging.error(f"Общая ошибка при выполнении задачи: {e}", exc_info=True)
        await bot.send_message(myChat, f"Критическая ошибка в задаче: {e}")
        
    try:
        for file_name in os.listdir(DOWNLOAD_FOLDER):
            if file_name.endswith('.xlsx') and "Троїцька".lower() in file_name.lower():
                file_path_local = os.path.join(DOWNLOAD_FOLDER, file_name)
                
                xml_file_name = "Троїцька.xml"
                
                try:
                    print(f"Обработка файла: {file_name}")
                    main_format(file_path_local, xml_file_name)
                    print(f"Файл '{file_name}' преобразован в '{xml_file_name}'.")

                    main_api(xml_file_name) 
                    print(f"Файл '{xml_file_name}' отправлен через API.")
                    
                    processed_files_count += 1
                    
                    notification_text = (
                        f"Задача по 'Троїцька' завершена. Время: {current_time_plus_3}\n"
                        f"Обработано файлов: {processed_files_count}\n"
                        f"Файл: {file_name}"
                    )
                except Exception as e:
                    print(f"Ошибка при обработке файла '{file_name}' в задаче: {e}", exc_info=True)
                    await bot.send_message(myChat, f"Ошибка при обработке '{file_name}': {e}")
        
        await bot.send_message(myChat, notification_text)
        logging.info(notification_text)

    except Exception as e:
        logging.error(f"Общая ошибка при выполнении задачи: {e}", exc_info=True)
        await bot.send_message(myChat, f"Критическая ошибка в задаче: {e}")


async def main():
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(hourly_task, 'interval', minutes=20) 




    scheduler.start()

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен.")
    except Exception as e:
        logging.error(f"Произошла непредвиденная ошибка при запуске бота: {e}", exc_info=True)