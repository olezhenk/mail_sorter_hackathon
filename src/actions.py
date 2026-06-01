#перемещение и распределение файлов по папкам Максим
import os
import shutil

class emailsort:
    def __init__(self,base):
        self.base=base
        self.statistika={}

    def sort_one(self,file,category):
        folder=os.path.join(self.base,category)

        if not os.path.exists(folder):
            os.makedirs(folder)

        name=os.path.basename(file)
        d=os.path.join(folder,name)

        shutil.move(file,d)
        print(f"Перемещено: {name} -> {category}")
        if category not in self.statistika:
            self.statistika[category] = 0
        self.statistika[category]+=1

    def sort_all(self,emails,classifier):
        for path,email in emails:
            cat = classifier.classify(email)
            self.sort_one(path,cat)
    def print_statistic(self):
        print("\nИтого:")
        for cat,count in self.statistika.items():
            print(f"{cat}:{count} писем")

