FROM node:18

WORKDIR /usr/src/app

COPY ./app/package*.json ./

RUN npm install

COPY ./app .

CMD [ "node", "index.js" ]