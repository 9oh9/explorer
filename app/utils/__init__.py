import csv
from datetime import datetime

def format_date(date_str):
    return datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')


def date_to_str(date):
    return date.strftime('%m/%d/%Y %H:%M:%S')


def write_csv(in_file, out_file):

    count = 0
    writable = []
    old_count = 0

    with open(out_file, 'w') as w_csvfile:

        fieldnames = [
            'pickup_time',
            'dropoff_time',
            'pickup_latlng',
            'dropoff_latlng'
        ]

        writer = csv.DictWriter(w_csvfile, fieldnames=fieldnames)
        writer.writeheader()

        csv_file = open(in_file);
        reader = csv.reader(csv_file, delimiter=' ')

        readable = list(reader);
        rl = len(readable)

        for i in range(2, rl, 2):

            last = (i == (rl - 1))

            pickup, dropoff = readable[i-1][0].split(','),\
                    readable[i][0].split(',')

            date1, date2 = format_date(pickup[0]), format_date(dropoff[0])

            if(date2 < date1):
                pickup, dropoff = dropoff, pickup


            wd = {}
            wd['pickup_time'] = pickup[0]
            wd['dropoff_time'] = dropoff[0]
            wd['pickup_latlng'] = 'POINT({} {})'.format(pickup[2], pickup[1])
            wd['dropoff_latlng'] = 'POINT({} {})'.format(dropoff[2], dropoff[1])

            writable.append(wd)

            count += 2

#            if count == 1:
            if count >= 450000:
                # write to file
                writer.writerows(writable)
                writable = []
                old_count = count + old_count
                perc_done = (old_count / rl) * 100
                count = 0


                print(
                    'You are {} percent done! {} of {} records.'.format(
                        str(perc_done),
                        str(old_count),
                        str(rl)
                    )
                )

        # reuse second to last record for odd number of records

        pickup, dropoff = readable[rl-2][0].split(','),\
                readable[rl-1][0].split(',')

        date1, date2 = format_date(pickup[0]), format_date(dropoff[0])

        if(date2 < date1):
            pickup, dropoff = dropoff, pickup


        wd = {}
        wd['pickup_time'] = pickup[0]
        wd['dropoff_time'] = dropoff[0]
        wd['pickup_latlng'] = 'POINT({} {})'.format(pickup[2], pickup[1])
        wd['dropoff_latlng'] = 'POINT({} {})'.format(dropoff[2], dropoff[1])

        writable.append(wd)

        # write to file
        writer.writerows(writable)
        writable = []
        old_count = count + old_count + 1
        perc_done = (old_count / rl) * 100
        count = 0

        print(
            'You are {} percent done! {} of {} records.'.format(
                str(perc_done),
                str(old_count),
                str(rl)
            )
        )
