FROM node:9.0

ENV APP /app
RUN mkdir -p $APP
WORKDIR $APP

COPY package.json .

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "start"]