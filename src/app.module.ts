import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PrivateModule } from './private/private.module';
import 'dotenv/config';

@Module({
  imports: [
    PrivateModule,
    MongooseModule.forRoot(process.env.DB_CONNECTION_URI),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
