import {
  Body,
  Controller,
  Delete,
  Get,
  Param,
  Post,
  Query,
} from '@nestjs/common';
import { sendHooksToMain } from './hooks/main.hook';
import { PrivateService } from './private.service';

@Controller('private')
export class PrivateController {
  constructor(private readonly privateService: PrivateService) {}

  @Get('/')
  getAllNotificationByTime(@Query('time') queryTime: number) {
    return this.privateService.getAllNotificationByTime(queryTime);
  }

  @Get('/:id')
  getAllNotificationById(@Param('id') userid: string) {
    return this.privateService.getAllNotificationById(userid);
  }

  @Post('/:id')
  addNotificationById(
    @Param('id') userid: string,
    @Body('time') time: number,
    @Body('subject') subject: string,
    @Body('notes') notes: string,
    @Body('username') username: string,
    @Body('avatarurl') avatarurl: string,
  ) {
    time = time || Number(Date.now());
    sendHooksToMain({ userid, subject, notes, time }, { username, avatarurl });
    return this.privateService.addNotificationById({
      userid,
      subject,
      notes,
      time,
    });
  }

  @Delete('/:userid')
  deleteNotificationByObjectId(
    @Param('userid') userid: string,
    @Query('id') objectId: string,
  ) {
    return this.privateService.deleteNotificationByObjectId(objectId);
  }
}
