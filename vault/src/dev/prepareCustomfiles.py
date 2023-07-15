import csv
import os

class preparefiles(object):
  def __init__(self,filepath='', file_type='csv', delimit=','):
    self.file_path = filepath
    self.file_type = file_type
    self.delimit = delimit if self.file_type == 'csv' else None
    self.csventries = [['Sno', 'birth_date', 'first_name', 'last_name',
              'created_date', 'ssn', 'credit_card_number', 'address', 'salary'],
              ['1', '2023-03-10', 'Ash Ketchum','Jr.', '2020-01-01T14:49:12.301977',
              '360-56-6750', '3600-5600-6750-0000', 'NY, NY',  '352200'],
              ['2', '2023-03-11',  'Lui Ken', 'Se', '2023-01-01T14:49:12.301977',
              '887-56-6786', '1823-4296-7852-0010','NY, NY', '80000'],
              ['3', '2023-03-12', 'Chang', 'Lee',  '2020-03-01T14:49:12.301977',
              '788-78-5670','7782-7787-7780-0011',  'NY, NY', '100000'],
              ['4', '2023-03-14', 'Xu',  'Yong', '2020-01-03T14:49:12.301977',
                '360-48-4198', '3600-5600-7889-1011',  'NY, NY',  '7788550'],
              [ '5',  '2023-03-15',  'Roberts',  'Henry','2021-01-01T14:49:12.301977',
                '122-66-7895',  '7330-8896-4799-1000',  'NY, NY',  '63300'],
              [ '6',  '2023-03-15',  'Keo',  'Lamn',  '2020-08-07T14:49:12.301977',
                '785-80-8860',  '8778-5600-6750-7892',  'NY, NY',  '78522'],
              ['7',  '2023-03-17', 'Sam', 'Eric', '2020-11-01T14:49:12.301977',
                '363-45-8755',  '5546-7752-7885-4296',  'NY, NY',  '455000'],
              [ '8',  '2023-03-18', 'Paul',  'Misor',  '2008-01-01T14:49:12.301977',
                '378-96-8777',  '9985-6630-8852-8432', 'NY, NY',  '100000'],
              [ '9', '2023-03-19', 'Richard',  'David',  '2014-01-01T14:49:12.301977',
                '870-06-6650', '7799-6630-6750-9732',  'NY, NY', '875200']
              ]

  def prepare_csv_file(self, filename, csventries):
    if not os.path.exists(self.file_path):
       os.makedirs(self.file_path)
    with open(os.path.join(self.file_path , filename), 'w', newline='') as file:
        writer = csv.writer(file, delimiter=self.delimit)
        # writer.writeheader()
        writer.writerows(csventries)
