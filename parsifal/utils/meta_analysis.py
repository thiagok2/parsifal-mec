# -*- coding: utf-8 -*-
from scipy import stats
from numpy import *
'''
Referencia para implementacao do calculo de tamanho de efeito

https://www.researchgate.net/profile/Helena_Espirito_Santo/publication/273143169_Calcular_e_apresentar_tamanhos_do_efeito_em_trabalhos_cientificos_1_As_limitacoes_do_p_005_na_analise_de_diferencas_de_medias_de_dois_grupos_Calculating_and_reporting_effect_sizes_on_scientific_papers/links/54fa10290cf2040df21b1b1c/Calcular-e-apresentar-tamanhos-do-efeito-em-trabalhos-cientificos-1-As-limitacoes-do-p-0-05-na-analise-de-diferencas-de-medias-de-dois-grupos-Calculating-and-reporting-effect-sizes-on-scientific-pap.pdf
'''
confidence_level = 0.95
#USO INTERNO APENAS
def extract_collumn(dataset, index):
    lst = []
    for i in dataset:
        lst.append(i[index])
    return lst
#USO INTERNO APENAS
def studies_names(dataset):
    return extract_collumn(dataset, 0)
#USO INTERNO APENAS
def effect_sizes(dataset):
    return extract_collumn(dataset, 1)
#USO INTERNO APENAS
def cis_min(dataset):
    return extract_collumn(dataset, 2)
#USO INTERNO APENAS
def cis_max(dataset):
    return extract_collumn(dataset, 3)
#USO INTERNO APENAS
def std_error(dataset):
    return extract_collumn(dataset, 4)
#USO INTERNO APENAS
#multiplica os i-esimos termos de cada conjunto, somando-os
#considera que ambos os conjuntos tem mesmo tamanho
def somarproduto(dataset1, dataset2):
    resultado = 0
    for i in range(0, len(dataset1)):
        resultado = resultado + dataset1[i] * dataset2[i]
    return resultado
#USO INTERNO APENAS
#multiplica os i-esimos termos de cada conjunto, somando-os
#considera que ambos os conjuntos tem mesmo tamanho
def somarproduto2(dataset1, dataset2, dataset3):
    resultado = 0
    for i in range(0, len(dataset1)):
        resultado = resultado + dataset1[i] * dataset2[i] * dataset3[i]
    return resultado
#USO INTERNO APENAS
#Soma os elementos de um conjunto
def somar(dataset):
    resultado = 0
    for i in dataset:
        resultado = resultado + i
    return resultado
#USO INTERNO APENAS
#Calcula o peso de cada estudo considerando o modelo de tamanho de efeito fixo
def weightf(dataset):
    std = std_error(dataset)
    result = []
    for i in std:
        result.append(1/i**2)
    return result
#USO INTERNO APENAS
def q(dataset):
    efs = effect_sizes(dataset)
    weightf_ = weightf(dataset)
    s1 = somarproduto2(weightf_, efs, efs)
    s2 = (somarproduto(weightf_, efs)**2)/somar(weightf_)
    return s1 - s2
#USO INTERNO APENAS
def t2(dataset):
    q_ = q(dataset)
    weightf_  = weightf(dataset)
    if (q_ - len(dataset)) <= 0:
        return 0
    else:
        return (q_ - (len(dataset) - 1)) / (somar(weightf_) - (somarproduto(weightf_, weightf_)/somar(weightf_)))
#USO INTERNO APENAS
def t(dataset):
    return t2(dataset)**0.5
#USO INTERNO APENAS
#Calcula o peso de cada estudo considerando o modelo de tamanho de efeito randomico
def weightr(dataset):
    result = []
    std = std_error(dataset)
    t2_ = t2(dataset)
    for i in std:
        result.append(1/(i**2+t2_))
    return result
#USO INTERNO APENAS
#Calcula o peso de cada estudo considerando percentual
def weightp(dataset):
    weightr_ = weightr(dataset)
    somar_ = somar(weightr_)
    result = []
    for i in weightr_:
        result.append(i / somar_)
    return result
#USO INTERNO APENAS
#Calcula o tamanho de efeito combinado
def effect_size_comb(dataset):
    weightr_ = weightr(dataset)
    efs = effect_sizes(dataset)
    return somarproduto(weightr_, efs)/somar(weightr_)
#USO INTERNO APENAS
def residual(dataset):
    efs = effect_sizes(dataset)
    result = []
    efs_comb = effect_size_comb(dataset)
    for i in efs:
        result.append(i - efs_comb)
    return result
#USO INTERNO APENAS
def std_error_efs_comb(dataset):
    weightr_ = weightr(dataset)
    residual_ = residual(dataset)
    #print 'std residual ', residual_
    k = len(dataset)
    #print 'zero?? ', ((k - 1)*somar(weightr_))
    return ((somarproduto2(weightr_, residual_, residual_))/((k - 1)*somar(weightr_)))**0.5
#Usar essa funcao para calcular o limiar minimo do tamanho de efeito combinado
def cin_efs_lower_limit(dataset):
    k = len(dataset)
    efs_comb = effect_size_comb(dataset)
    std_comb = std_error_efs_comb(dataset)
    return efs_comb - abs(stats.t.ppf(1-(1-confidence_level)/2, k - 1))*std_comb
#Usar essa funcao para calcular o limiar maximo do tamanho de efeito combinado
def cin_efs_max_limit(dataset):
    k = len(dataset)
    efs_comb = effect_size_comb(dataset)
    std_comb = std_error_efs_comb(dataset)
    return efs_comb + abs(stats.t.ppf(1-(1-confidence_level)/2, k - 1))*std_comb
'''
Implementa o calculo do tamanho de efeito via Cohen D

Uso: Grupos independentes / DP similares

Entradas:
    n1 => tamanho da amostra do grupo 1
    dp1 => desvio padrao do grupo 1
    n2 => tamanho da amostra do grupo 2
    dp2 => desvio padrao do grupo 2
    m1 => media do grupo 1
    m2 => media do grupo 2

Saida:
    cohen_d => tamanho de efeito segundo metodo Cohen's D
    CImin => limite minimo intervalo de confiana
    CImax => limite maximo intervalo de confiana
    std_error => erro padrão combinado

'''
def cohen_d(n1, dp1, n2, dp2, a1, a2):
    dp_comb = ((n1 - 1) * dp1**2 + (n2 - 1) * dp2**2)/(n1 + n2 - 2)
    c_d = (a1 - a2) / dp_comb
    ci = float((((n1 + n2) / (n1 * n2))+ ((c_d**2) / (2 * (n1 + n2)))))**0.5

    result = {
        "cohen_d" : float(c_d),
        "ci_min" : (float(c_d) - 1.96*ci),
        "ci_max" : (float(c_d) + 1.96*ci),
        "std_error": float(dp_comb)
    }

    print 'resulttt ', result
    return result
#Modelo de dados padrao a ser trabalhado para o calculo de tamanho de efeito combinado
#modelo padrao de tamanho de efeito considerando o tamanho de efeito e tamanho de erro padrao
dataset = [
#[estudo, effect_size, ci_min, cin_max, standard-error]
['aaaa', 2.2, 1.699645618, 2.700354382, 0.252167174],
['bbbb', 1.8, 1.390343029, 2.209656971, 0.207051756],
['cccc', 1.9, 1.367384352, 2.432615648, 0.267585517],
['dddd', 2.05, 1.769818748, 2.330181252, 0.14237361],
['eeee', 0.05, -0.354749802, 0.454749802, 0.203850427],
['ffff', -0.6, -1.024709892, -0.175290108, 0.213746575],
['gggg', 2.00, 1.559114969, 2.440885031, 0.222657976],
['hhhh', 1.8, 1.390343029, 2.209656971, 0.207051756],
['iiii', 0.4, -0.045254008, 0.845254008, 0.223695125],
['jjjj', 2.1, 1.783894704, 2.416105296, 0.160464477],
['kkkk', -0.40, -0.819513685, 0.019513685, 0.211131446],
['llll', -0.50, -0.899997093, -0.100002907, 0.201589394]
]
# print("EFS_comb: " + str(effect_size_comb(dataset)))
# print(cin_efs_lower_limit(dataset))
# print(cin_efs_max_limit(dataset))
#Passos para calculo:
#  1. para cada trabalho calcular o cohen D (tamanho de efeito, min, max)
#  2. calcular o tamanho de efeito combinado
#  3. Invocar o servico REST para recuperacao do grafico
#  4. Utilizar o campo effect_size de cada trabalho para gerar a interpretacao, levando em consideracao o modelo de interpretacao (Cohen ou Hattie)
