from aiogram.types import Message
from data.loader import bot, dp, db
from states.states import NumberState
from aiogram.dispatcher import FSMContext
import re
from keyboards.reply import generate_main_menu, \
    generate_delivery_type, generate_filials, generate_categories

async def start_register(message: Message, state=None):
    await NumberState.phone.set()
    await message.answer('Отправьте свой номер телефона в формате: <b>+998 ** *** ** **</b>')

@dp.message_handler(state=NumberState.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text
    result1 = re.search(r'\+998 \d\d \d\d\d \d\d \d\d', phone)
    result2 = re.search(r'\+998\d{9}', phone)
    if result1 or result2:
        await message.answer('Ок')
        chat_id = message.chat.id
        full_name = message.from_user.full_name
        await state.finish()
        db.insert_user(chat_id, full_name, phone)
        await show_main_menu(message)
    else:
        await message.answer('No')
        await state.finish()
        await again_start_register(message)


async def again_start_register(message: Message, state=None):
    await NumberState.phone.set()
    await message.answer('''Неверный номер телефона или запись. 
Напишите в этом формате: <b>+998 ** *** ** **</b>''')

@dp.message_handler(regexp='◀ Главное меню')
async def show_main_menu(message: Message):
    await message.answer('Выберите раздел: ', reply_markup=generate_main_menu())

# @dp.message_handler(regexp='⚙ Настройки')



@dp.message_handler(regexp='🛍 Заказать')
@dp.message_handler(regexp='◀ К выбору доставки')
async def choice_delivery(message: Message):
    await message.answer('Заберите свой заказ самостоятельно 🙋‍♂\nили выберите доставку 🚙',
                         reply_markup=generate_delivery_type())


@dp.message_handler(regexp='🏃 Самовывоз')
async def choice_filial(message: Message):
    await message.answer('Выберите филиал', reply_markup=generate_filials())


filials = [i[0] for i in db.get_filials()] # ['максимка', 'чорсу']

@dp.message_handler(lambda message: message.text in filials)
async def show_menu(message: Message):
    await message.answer('Выберите категорию: ', reply_markup=generate_categories())


