# gerekli paketleri(kütüphaneleri) içe aktarıyoruz
import argparse

# terminalden argüman girişi alabilmek için argaparse kütüphanesi kullanıyoruz
ap = argparse.ArgumentParser()                         # ArgumentParser sınıfını ap değişkenine atıyoruz 
ap.add_argument("-n", "--name", required=True,help="kullanicinin adi")  # ap değişkeninin add_argument fonksiyonunu kullanarak alacağımız argümanları belirliyoruz.
args = vars(ap.parse_args())

# kulanıcıya dostca bir mesaj gönderiyoruzz :)
print("Merhaba {}, tanistigimiza memnun oldum!".format(args["name"]))

