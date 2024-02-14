from clienttracker.db.crud import *

create_tables()

insert_clients([Client(first_name=f'{i}', last_name='Клиент', vk_link='etoslozhn0' if i == 0 else None) for i in range(10)])

