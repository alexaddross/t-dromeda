def bags_formatter(robot_data):
    return f'''<b>Информация о мешках</b>
    
            Всего уложено мешков: {robot_data["total_bags"]}
            Уложено мешков за текущею смену: {robot_data["shift_bags"]}
            '''
