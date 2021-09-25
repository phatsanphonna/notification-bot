import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { PrivateController } from './private.controller';
import { PrivateRespository } from './private.repository';
import { PrivateService } from './private.service';
import { Private, PrivateSchema } from './schema/private.schema';

@Module({
  imports: [
    MongooseModule.forFeature([
      {
        name: Private.name,
        schema: PrivateSchema,
      },
    ]),
  ],
  controllers: [PrivateController],
  providers: [PrivateService, PrivateRespository],
})
export class PrivateModule {}
