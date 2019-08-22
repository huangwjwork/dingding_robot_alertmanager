t1 = '2019-08-18T09:34:31.345816455Z'
t1 = t1[0:26] + 'T'

# print('1', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
# print('2', t1[0:26])
# timearray = time.strptime(t1[0:26], '%Y-%m-%dT%H:%M:%S.%f')
# print(timearray)
# t2 = time.strftime('%Y-%m-%d %H:%M:%S.%fZ', timearray)
# print(t1, t2)
t1.replace(' ', 'T', 1)
t1 += 'Z'
print(t1)