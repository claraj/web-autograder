# turn raw data into
# id, github, name

# or id, ,name

import re

alldata = []

with open('raw_spring_2018.txt') as f:

    for line in f:
        # example
        # Aaron Souer Not flagged - Click to flag	Aaron SouerAaron Souer is online	00282000	Student
    	#line = line.strip()

        if 'Student' not in line:
            continue

        print(line)
        name_end_txt = 'Not flagged - Click to flag'
        end_of_name = line.find(name_end_txt)
        name = line[0:end_of_name]
        name = name.strip()
        # regex, 8 digit number

        regex = '\\d{8}'
        id = re.findall(regex, line )[0]
        print(id)

        out_line = '%s, ,%s' % (name, id)

        print(out_line)

        alldata.append(out_line)


with open('class_data.txt', 'w') as f:
    for line in alldata:
        f.write(line)
        f.write('\n')
    f.close()
