import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

@Schema({ collection: 'private-alert' })
export class Private {
  @Prop({ required: true })
  userid: string;
  @Prop({ required: true })
  time: number;
  @Prop({ required: true })
  subject: string;
  @Prop({ required: false, default: '-' })
  notes: string;
}

export type PrivateDocument = Private & Document;

export const PrivateSchema = SchemaFactory.createForClass(Private);
