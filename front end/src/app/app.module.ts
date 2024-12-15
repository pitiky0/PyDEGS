import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RegisterComponent } from './register/register.component';
import { ProfileComponent } from './profile/profile.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { AuthService } from './_services/auth.service';
import { ChangePasswordComponent } from './profile/change-password/change-password.component';
import { VerifyEmailComponent } from './profile/verify-email/verify-email.component';
import { DeleteComponent } from './profile/delete/delete.component';
import { FormsModule } from '@angular/forms';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { EditProfileComponent } from './profile/edit-profile/edit-profile.component';


import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';


import { ListFilesComponent } from './upload/list-files/list-files.component';
import { UploadFileComponent } from './upload/upload-file/upload-file.component';
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
import { DiffExpressionResultsComponent } from './diff-expression/diff-expression-results/diff-expression-results.component';
import { KeyValuePipe } from './key-value.pipe';





@NgModule({
  declarations: [
    AppComponent,
    KeyValuePipe,
    RegisterComponent,
    LoginComponent,
    ProfileComponent,
    HomeComponent,
    ForgotPasswordComponent,
    ChangePasswordComponent,
    VerifyEmailComponent,
    DeleteComponent,
    ResetPasswordComponent,
    EditProfileComponent,


    UploadFileComponent,
    ListFilesComponent,
    QualityControlComponent,


    ListQCFilesComponent,
        FilteringComponent,
        ListFilteringFilesComponent,
        AlignmentComponent,
        ListAlignmentFilesComponent,
        FileDetailsComponent,
        FileFilteringDetailsComponent,
        QuantificationComponent,
        ListQuantificationComponent,
        DiffExpressionComponent,
        DiffExpressionResultsComponent



  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatCardModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    MatSelectModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatToolbarModule,
    MatInputModule,
    MatButtonModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [AuthService,  provideAnimationsAsync()],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  bootstrap: [AppComponent]
})
export class AppModule { }
