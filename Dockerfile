FROM node:10

WORKDIR /app
VOLUME /app/static

# Installing dependencies
COPY alfred-fe/package*.json /app/
RUN npm install

# Copying source files
COPY alfred-fe /app

# Building app
RUN npm run build

# Running the app
CMD [ "npm", "start" ]
