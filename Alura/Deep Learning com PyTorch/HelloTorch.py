import torch
import numpy as np

def print_test(test: str):
    print("")
    print("###########################################")
    print("# " + test)
    print("###########################################")

print_test("Criando tensores A partir de listas")

ll = [[1, 2, 3], [4, 5, 6]]
tns = torch.Tensor(ll)
print(tns.dtype)
print(tns)

tns = torch.DoubleTensor(ll)
print(tns.dtype)
print(tns)

tns = torch.LongTensor(ll)
print(tns.dtype)
print(tns)

# atraves do numpy
print_test("Criando tensores A partir do numpy")

arrfloat = np.random.rand(3,4)
arrint = (arrfloat*10).astype(int)

tsnfloat = torch.from_numpy(arrfloat)
tsnint = torch.from_numpy(arrint)

print(arrfloat)
print(arrint)
print(tsnfloat)
print(tsnint)

print_test("Inicializando tensores")

tsn1 = torch.ones(2, 3)
tsn0 = torch.zeros(4, 5)
tsnr = torch.randn(3, 3)

print(tsn1)
print(tsn0)
print(tsnr)


tsnr = torch.randn(3, 3)
arr = tsnr.data.numpy()
print(arr)


tsnr = torch.randn(3, 3)
arr = tsnr.data.numpy()
print(tsnr)
tsnr[0, 2] = -10
print(tsnr)
print(tsnr[0:2, 1:3])


# tsnr1 = torch.ones(2, 2, 3)
tsnr1 = torch.rand(2, 2, 3)

print("--")
print(tsnr1.shape)
print("--")
print(tsnr1.size())

tsnr1_view = tsnr1.view(12)
print("--")
print(tsnr1_view)
print("--")
print(tsnr1)

print_test("HARDWARE TEST")

if torch.cuda.is_available():
  device = torch.device('cuda')
else:
  device = torch.device('cpu')
print(device)






