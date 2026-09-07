'''

write a game scoring system that saves a players name and score to a file. each time the program runs, load exsisting scores and display top 3

'''

class ScoringSystem:
    def __init__(self):
        try:
            f = open('scores.txt', 'r')
            try:
                print(f.readlines()[2])
            except IndexError:
                for x in f.readlines():
                    print(x)
            f.close()
        except FileNotFoundError:
            file = open('scores.txt', 'w')
            file.close()
        self.true = True
        self.shhhhhhhhhhh = ''
        self.temp = []

    def save_score(self,name,score):
        f = open('scores.txt', 'r')
        count = -1
        for x in f.readlines():
            count += 1
            if score > int(x.split(':')[1]):
                try:
                    #self.temp = f.readlines().insert(count, x+'\n')
                    self.temp = f.readlines()
                    self.temp.insert(count,x+'\n')
                    for i in self.temp:
                        self.shhhhhhhhhhh += f"{name} :"+i
                except IndexError:
                    #self.temp = f.readlines().append(x + '\n')
                    self.temp = f.readlines()
                    self.temp.append(x + '\n')
                    for i in self.temp:
                        self.shhhhhhhhhhh += f"{name} :"+i
        print(self.shhhhhhhhhhh)
        f.close()

main = ScoringSystem()
while main.true:
    main.save_score(input('Enter your name:'),int(input('Enter your score:')))
    file = open('scores.txt', 'w')
    file.write("")
    file.write(main.shhhhhhhhhhh)
    file.close()
    main.true = False if input('Do you wish to continue? (y/n) ') != 'y' else True
