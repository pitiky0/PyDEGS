// src/app/_models/user.model.ts
export interface User {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  gender: string;
  birthdate: string;
  about_me: string;
  image_url?: string; // Add any other optional fields as needed
}


// models/user.ts
export enum Gender {
    Male = 'Male',
    Female = 'Female',
    Other = 'Other'
  }