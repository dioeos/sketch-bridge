export interface APIErrorDetail {
  message: string;
  content?: string;
}

export interface APIError {
  message: string | APIErrorDetail;
}
