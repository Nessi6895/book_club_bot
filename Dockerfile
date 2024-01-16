FROM python:3.8-slim-buster
ADD src src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ARG API_TOKEN
ARG ADMIN_USER_ID
ARG CLUB_CHAT_ID
ENV ADMIN_USER_ID=$ADMIN_USER_ID
ENV API_TOKEN=$API_TOKEN
ENV CLUB_CHAT_ID=$CLUB_CHAT_ID
CMD [ "python", "src/main.py" ]