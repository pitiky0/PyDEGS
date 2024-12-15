import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'keyValue' })
export class KeyValuePipe implements PipeTransform {
  transform(value: any, ...args: any[]): any {
    if (value && typeof value === 'object') {
      return Object.keys(value).map(key => ({ key, value: value[key] }));
    }
    return [];
  }
}
