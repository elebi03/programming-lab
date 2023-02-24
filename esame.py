# creo classe per eccezioni da alzare in caso di input non corretti
class ExamException(Exception):
    pass


class CSVTimeSeriesFile():

    def __init__(self, name = None): #setto name a None come valore di default nel caso in cui l'utente non passa nessun valore

        # setto il nome del file tramite la variabile name
        self.name = name

    # creo metodo che torna una lista di due liste dove la prima è la data, la seconda è il numero di passeggeri
    def get_data(self):

        # provo ad aprirlo e leggere una linea
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except:
            raise ExamException("Impossibile leggere il file")

        # inizializzo una lista vuota per salvare tutti i dati
        time_series = []

        # apro il file
        try:
            my_file = open(self.name, 'r')
        except:
            raise ExamException('File illeggibile o inesistente')

        # leggo il file linea per linea
        for line in my_file:

            # pulisco il carattere di newline e faccio lo split di ogni linea sulla virgola
            try:
                elements = line.strip('\n').split(',')
            except:
                raise ExamException('Formato della linea non è corretto')

            # garantisco che la linea di testo letta dal file contenga almeno i due elementi
            if len(elements) < 2:
                continue

            date = elements[0]
            
            # verifico che che linea di testo letta dal file non contenente la data venga saltata
            if not "-" in date:
                continue
            
            # creo lista di due stringhe, ovvero mese e anno 
            date_splitted = date.split("-")
            
            # verifico la lista contenga solo due elementi
            if len(date_splitted) != 2:
                continue
            
            try:
                int(date[0])
                month = int(date[1])
                if month < 1 or month > 12:
                    continue
            except:
                continue
            
            try:
                passengers = int(elements[1])
                if passengers < 0:
                    continue
            except:
                continue
            
            time_series.append([date, passengers])
                
        # chiudo il file
        my_file.close()

        # verifico se la serie temporale è disordinata o duplicata confrontando data del punto i-esimo della serie temporale (sottolista i)in posizione 0 (data), ovvero se 
        # time_series = [['2020-01', 100], ['2020-02', 200]] allora time_series[0][0] corrisponde a '2020-01'
        for i in range(len(time_series) - 1):
            if time_series[i][0] >= time_series[i + 1][0]: 
                raise ExamException('Date non ordinate o duplicate')

        # quando ho processato tutte le righe, ritorno i dati
        return time_series


def detect_similar_monthly_variations(time_series, years):
    # verifico che years contenga due anni
    if len(years) != 2:
        raise ExamException
    
    year1 = years[0]
    year2 = years[1]
    
    #verifico che gli anni siano interi
    try:
        year1 = int(year1)
        year2 = int(year2)
    except:
        raise ExamException
    
    #verifico che ci siano dati per entrambi gli anni inseriti con flag 
    years1_exists = False
    years2_exists = False
    for item in time_series:
        y = int(item[0].split("-")[0])
        if y == year1:
            years1_exists = True
        if y == year2:
            years2_exists = True
            
    if not years1_exists or not years2_exists:
        raise ExamException
    
    # creo due liste da 12 elementi per ogni anno dove elemento indice m corrisponde a numero di passeggeri per mese m+1 in quell’anno e le inizializzo a None
    year1_data = [None for i in range(12)]
    year2_data = [None for i in range(12)]
    
    for item in time_series:
        y = int(item[0].split("-")[0]) # estraggo l'anno dalla stringa contenente la data 
        m = int(item[0].split("-")[1]) # estraggo il mese dalla stringa contenente la data 
        
        if y == year1:
            year1_data[m-1] = item[1] #m-1 in quanto gli index partono da zero mentre i mesi da 1 
            
        elif y == year2:
            year2_data[m-1] = item[1]
    
    # creo due liste con le 11 differenze del numero di passeggeri tra ogni coppia di mesi dello stesso anno e le inizializzo a None
    year1_diff = [None for i in range(11)]
    year2_diff = [None for i in range(11)]
    
    # ciclo sui dodici mesi faccendo la differenza nel caso in cui i dati sono stati riempiti 
    for i in range(11):
        if year1_data[i] != None and year1_data[i+1] != None:
            year1_diff[i] = year1_data[i+1] - year1_data[i]
        
        if year2_data[i] != None and year2_data[i+1] != None:
            year2_diff[i] = year2_data[i+1] - year2_data[i]
            
    # creo lista che conterrà i risultati 
    result = []
    
    # ciclo sulle undici differenze paragonando i valori ottenuti per ogni coppia di mesi tra i due anni e valutando se c’è una variazione (False) o se è uguale con una tolleranza di ±2 (True)
    for i in range(11):
        if year1_diff[i] == None or year2_diff[i] == None:
            result.append(False)
        elif abs(year1_diff[i] - year2_diff[i]) <= 2:
            result.append(True)
        else:
            result.append(False)
    
    return result
