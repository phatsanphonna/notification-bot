import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Private, PrivateDocument } from './schema/private.schema';

@Injectable()
export class PrivateRespository {
  constructor(
    @InjectModel(Private.name) private privateModel: Model<PrivateDocument>,
  ) {}

  async findByQueryTime(queryTime: number): Promise<Private[]> {
    return this.privateModel.find({ time: { $lte: queryTime } });
  }

  async findById(userid: string): Promise<Private[]> {
    return this.privateModel.find({ userid });
  }

  async findByIdAndDelete(objectId: string): Promise<Private> {
    return this.privateModel.findByIdAndDelete(objectId);
  }

  async create(notificationData: Private): Promise<Private> {
    const newNotification = new this.privateModel(notificationData);
    return newNotification.save();
  }
}
