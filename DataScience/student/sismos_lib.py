import pandas as pd
import matplotlib.pyplot as plt

def calc_numero_de_sismos(filename):
    """
    Calcula el número de sismos en una determinada fecha usando información del
    Servicio Sismológico Nacional (SSN).
    
    Parameters
    ----------
    filename. string
    Archivo en formato CSV obtenido del Catálogo de sismos del SSN.
    
    Returns
    -------
    cuenta_sismos. dict
    Diccionario con las fechas y años en que ocurrieron los sismos.
    
    numero_sismos. dict
    Diccionario con las fechas y número de sismos ocurridos en la misma.
    """
    ssn_frame = pd.read_csv(filename, header=4, skipfooter=7, engine='python')
    cuenta_sismos = {}
    for i in ssn_frame.Fecha:
        if i[5:] in cuenta_sismos.keys():
            cuenta_sismos[i[5:]].append(i[:4])
        else:
            cuenta_sismos[i[5:]] = [i[:4]]

    numero_sismos = {}
    for key in cuenta_sismos.keys():
        numero_sismos[key] = len(cuenta_sismos[key])

    return cuenta_sismos, numero_sismos



def plot_sismos(filename, magnitud_fecha):
    """
    Calcula el número de sismos en una determinada fecha usando información del
    Servicio Sismológico Nacional (SSN) y posteriormente realiza una gráfica
    con toda esta información.
    
    Parameters
    ----------
    filename. string
    Archivo en formato CSV obtenido del Catálogo de sismos del SSN.
    
    magnitud_fecha. string
    Cadena de texto con la información del intervalo de las magnitudes de los sismos 
    las fechas en que ocurrieron. Por ejemplo: '6 a 9 de 1900 a 2022'
    """
    _, magnitud = calc_numero_de_sismos(filename)
    
    df_magnitud = pd.DataFrame.from_dict(dict(sorted(magnitud.items())), orient='index')

    # Ubicación de los ticks en el eje x
    meses_ticks = [0]
    num_mes = 1
    for i,fec in enumerate(df_magnitud.index):
        if fec[0:2] != str('{:02d}'.format(num_mes)):
            meses_ticks.append(i)
            num_mes += 1
    meses_ticks.append(len(df_magnitud.index)-1)
    
    # Ubicación del máximo
    magnitud_sorted = dict(sorted(magnitud.items())) # Diccionario ordenado
    ymax = max(magnitud.values()) # Valor máximo de sismos
    xmax_string = max(magnitud_sorted, key=magnitud_sorted.get) # Fecha del máximo (string)
    xmax = list(magnitud_sorted.keys()).index(xmax_string) # Índice del máximo para graficación

    # Creamos una figura
    fig = plt.figure()

    # Graficamos usando plot de DataFrame
    df_magnitud.plot(kind='area', legend=False,
                     xlabel = 'Fechas [mes-día]', ylabel = 'Núm. de sismos', 
                     xticks=meses_ticks, rot=45,
                     figsize = (10,6), fontsize=10, 
                     alpha=0.5, color='C2')#, marker='.')

    # Decoramos la gráfica desde el nivel Artist 
    ax = plt.gca()

    # Eliminamos algunas líneas del marco
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Graficamos el máximo
    ax.scatter(xmax, ymax, c='red', ec='gray', alpha=0.75, zorder=5)

    # Hacemos algunas anotaciones para identificar el máximo
    ax.annotate('Máximo ({})'.format(ymax), (xmax*0.99, ymax), (xmax*0.65, ymax*0.95),
               arrowprops = dict(facecolor='gray', edgecolor='gray', width=0.25, headwidth=4.5, headlength=5.0))
    ax.axvline(x=xmax, ymax=0.95, ls='--', lw=1.5, c='C10') # Línea vertical
    ax.text(xmax*1.01, ymax*1.01, xmax_string, c='#aa1122') # Texto con la fecha del máximo

    # Título y subtítulo
    plt.suptitle('Número de sismos de magnitud {}'.format(magnitud_fecha), y = 0.98, fontsize=16)
    plt.title('Fuente: DOI: 10.21766/SSNMX/EC/MX', c='C0', loc='right', fontsize=10)

    # La rejilla de la gráfica
    plt.grid()
    plt.tight_layout()
    plt.savefig('sismos_reporte.pdf')

    plt.show()
    
    
if __name__ == '__main__':
    
    plot_sismos('../Datos/SSNMX_catalogo_19001001_20221011_m60_99.csv', '6 a 9 de 1900 a 2022')
