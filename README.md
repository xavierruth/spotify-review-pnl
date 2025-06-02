
# 🎧 Spotify Review PNL

Classificação automática de reviews de usuários do app Spotify na Play Store utilizando **Processamento de Linguagem Natural (PLN)** com o modelo **BERT**.


## Escopo

O objetivo deste projeto é prever a nota (Rating) de 1 a 5 que um usuário daria ao Spotify com base apenas em seu comentário (Review), utilizando modelos de classificação baseados em aprendizado profundo.

**Dataset:**  
Coletado via *scraping* de reviews do app Spotify na Play Store, entre 31/12/2021 e 09/07/2022.  
📥 [Download do dataset](https://www.kaggle.com/datasets/mfaaris/spotify-app-reviews-2022)

**Colunas:**
- `Time_stempped`: Data e hora do comentário
- `Rating`: Nota atribuída (1 a 5 estrelas)
- `Total_thumbsup`: Likes do comentário
- `Reply`: Resposta do Spotify
- `Review`: Texto do comentário

> O dataset original não contém rótulos explícitos de sentimento. A análise é baseada na previsão da nota (Rating), que serve como proxy do sentimento.


## Modelagem

### Pré-processamento:
- **Tokenização:** `TweetTokenizer` (NLTK)
- **Remoção de Stopwords**
- **Stemming:** `SnowballStemmer` (Inglês)
- **Vetorização:** `TfidfVectorizer`

### Modelo:
- **Arquitetura:** `BertForSequenceClassification` (pré-treinado com `bert-base-uncased`)
- **Número de classes:** 5 (Notas de 1 a 5)
- **Épocas:** 3
- **Batch size:** 16
- **Framework:** Hugging Face `transformers` + `Trainer`

### Avaliação:
- Acurácia
- Precisão
- Recall


##  Como Executar

1. Crie um ambiente virtual: 

``` bash 

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Instale as dependências com:

```bash
pip install -r requirements.txt
```

3. Crie o arquivo `.env` e adicione suas credenciais: 

``` bash
HF_API_KEY=seu_token_huggingface
FIREBASE_KEY=caminho/para/seu/firebase.json
# e outras keys que sejam importantes para o seu projeto
```
4. Execute o projeto: 

``` bash
python app.py
```

## Tecnologias 

- Flask
- Firebase
- Docker
- Hugging Face

## Links Importantes
- [Modelo Treinado no Hugging Face](https://huggingface.co/xavierruth/spotify-pnl)
- [Interface de Predição no Hugging Face](https://huggingface.co/spaces/xavierruth/spotify-review)
- [Notebook de Treinamento - Gooogle Colab](https://colab.research.google.com/drive/1zSxlUUhygHIBsf_69PfFCi0wTN4ObthX?usp=sharing)
- [Notebook de Visualizações - Google Colab](https://colab.research.google.com/drive/1jOsDkK9Tfr2Ev1ilY0DZox3BA9YxA-sf?usp=sharing)

## Futuras Melhorias 

- Durante a organização e limpeza dos dados, não foi feita inicialmente o balanceamento dos dados, o que gastou muito tempo para entender o que havia de errado e porque o modelo estava enviesado ou overfitted para duas classes: 1 e 5, que tinham muito mais registros;
- Pesquisar e testar outros modelos pré-treinados que demandem menos da máquina;
- Fazer uma lista inicial do que precisa ser feito na organização e limpeza dos dados para evitar retrabalho.


## Time

### Juliane Reis - Gestão de Projetos e Desenvolvedora Back-end
- [Linkedin](https://www.linkedin.com/in/julianereism/)
- [Github](https://github.com/julianereism)

### Ruth Xavier - UI/UX Designer e Desenvolvedora Front-end
- [Linkedin](https://www.linkedin.com/in/ruthxavier/)
- [Github](https://github.com/xavierruth)
- [Behance](https://www.behance.net/xavierruth)

### Matheus Custódio - QA
- [Linkedin](https://www.linkedin.com/in/custodiomatheus/)
- [Github](https://github.com/Mathueshcustodio)