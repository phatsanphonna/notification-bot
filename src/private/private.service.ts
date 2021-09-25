import { Injectable } from '@nestjs/common';
import { PrivateRespository } from './private.repository';
import { Private } from './schema/private.schema';

export interface data {
  userid: string;
  time: number;
  subject: string;
  notes: string;
}

export interface user {
  username: string;
  avatarurl: string;
}

@Injectable()
export class PrivateService {
  constructor(private readonly privateRepository: PrivateRespository) {}

  async getAllNotificationByTime(queryTime: number): Promise<Private[]> {
    return this.privateRepository.findByQueryTime(queryTime);
  }

  async getAllNotificationById(id: string): Promise<Private[]> {
    return this.privateRepository.findById(id);
  }

  async addNotificationById(data: data): Promise<Private> {
    return this.privateRepository.create(data);
  }

  async deleteNotificationByObjectId(objectId: string): Promise<Private> {
    return this.privateRepository.findByIdAndDelete(objectId);
  }
}
