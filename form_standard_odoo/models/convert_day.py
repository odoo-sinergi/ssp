

def get_day(date, bhs):
    day = ''
    if date:
        date_en = date.strftime('%m')
        if bhs == 'id':
            if date_en == "01":
                day = 'Januari'
            if date_en == "02":
                day = 'Febuari'
            if date_en == "03" :
                day = 'Maret'
            if date_en == "04":
                day = 'April'
            if date_en == "05":
                day = 'Mei'
            if date_en == "06":
                day = 'Juni'
            if date_en == "07":
                day = 'Juli'
            if date_en == "08":
                day = 'Agustus'
            if date_en == "09":
                day = 'September'
            if date_en == "10":
                day = 'Oktober'
            if date_en == "11":
                day = 'November'
            if date_en == "12":
                day = 'Desember'
        elif bhs == 'en':
            day = date_en

    return day


