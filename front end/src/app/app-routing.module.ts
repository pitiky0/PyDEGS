import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { ProfileComponent } from './profile/profile.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { ChangePasswordComponent } from './profile/change-password/change-password.component';
import { VerifyEmailComponent } from './profile/verify-email/verify-email.component';
import { DeleteComponent } from './profile/delete/delete.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { EditProfileComponent } from './profile/edit-profile/edit-profile.component';

import { UploadFileComponent } from './upload/upload-file/upload-file.component';

import { ListFilesComponent } from './upload/list-files/list-files.component';
import { QualityControlComponent } from './quality-control/quality-control.component';
import { ListQCFilesComponent } from './quality-control/list-qc-files/list-qc-files.component';

import { FilteringComponent } from './filtering/filtering.component';
import { ListFilteringFilesComponent } from './filtering/list-filtering-files/list-filtering-files.component';
import { AlignmentComponent } from './alignment/alignment.component';
import { ListAlignmentFilesComponent } from './alignment/list-alignment-files/list-alignment-files.component';

import { FileDetailsComponent } from './file-details/file-details.component';
import { FileFilteringDetailsComponent } from './file-filtering-details/file-filtering-details.component';
import { QuantificationComponent } from './quantification/quantification.component';
import { ListQuantificationComponent } from './quantification/list-quantification/list-quantification.component';
import { DiffExpressionComponent } from './diff-expression/diff-expression.component';
import {
  DiffExpressionResultsComponent
} from "./diff-expression/diff-expression-results/diff-expression-results.component";


const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'profile', component: ProfileComponent},

  { path: 'profile/change-password', component: ChangePasswordComponent },
  { path: 'profile/edit-profile', component: EditProfileComponent },
  { path: 'profile/verify-email', component: VerifyEmailComponent },
  { path: 'profile/delete', component: DeleteComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'reset-password', component: ResetPasswordComponent },

  { path: 'Upload-file', component: UploadFileComponent },

  { path: 'list-files', component: ListFilesComponent },
  { path: 'quality-control', component: QualityControlComponent },

  { path: 'list-qc-files', component: ListQCFilesComponent },
  { path: 'filtering', component:   FilteringComponent },
  { path: 'list-filtering-files', component:   ListFilteringFilesComponent },
  { path: 'alignment', component:   AlignmentComponent },

  { path: 'list-alignment-files', component:   ListAlignmentFilesComponent },
  { path: 'file-details/:fileName', component:   FileDetailsComponent },
  { path: 'file-filtering-details/:fileName', component:   FileFilteringDetailsComponent },
  { path: 'quantification', component:   QuantificationComponent },
  { path: 'list-quantification', component:   ListQuantificationComponent },
  { path: 'diff-expression', component:   DiffExpressionComponent  },
  {path: 'diff-expression-results', component: DiffExpressionResultsComponent },
  { path: '', redirectTo: 'home', pathMatch: 'full' } // Redirect to login as the default route
  // Add other routes here as needed
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
