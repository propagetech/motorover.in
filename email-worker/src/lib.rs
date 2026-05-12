use worker::*;
use serde::{Deserialize, Serialize};

mod utils;

#[derive(Deserialize, Serialize)]
struct FormData {
    name: String,
    email: String,
    message: String,
    form_type: String,
    recaptcha_token: String,
    phone: Option<String>,
}

#[event(fetch)]
pub async fn main(req: Request, env: Env, _ctx: worker::Context) -> Result<Response> {
    let router = Router::new();

    router
        .post_async("/api/submit", |mut req, ctx| async move {
            let cors_headers = cors();
            
            let form_data: FormData = match req.json().await {
                Ok(data) => data,
                Err(_) => return Response::error("Invalid JSON", 400).and_then(|r| r.with_headers(cors_headers.clone())),
            };

            // Validation
            if form_data.name.is_empty() || form_data.email.is_empty() {
                return Response::error("Missing required fields", 400).and_then(|r| r.with_headers(cors_headers.clone()));
            }

            // Recaptcha Verification
            let recaptcha_secret = match ctx.var("RECAPTCHA_SECRET_KEY") {
                Ok(v) => v.to_string(),
                Err(_) => "placeholder".to_string(),
            };

            if recaptcha_secret != "placeholder" {
                match utils::verify_recaptcha(&recaptcha_secret, &form_data.recaptcha_token).await {
                    Ok(valid) => {
                        if !valid {
                            return Response::error("Bot detected", 403).and_then(|r| r.with_headers(cors_headers.clone()));
                        }
                    },
                    Err(e) => console_error!("Recaptcha error: {}", e),
                }
            }

            // Get PDF Link
            let pdf_link = utils::get_pdf_link(&form_data.form_type);

            // Send Emails
            let sendgrid_key = match ctx.var("SENDGRID_API_KEY") {
                Ok(v) => v.to_string(),
                Err(_) => "placeholder".to_string(),
            };
            
            let owner_email = match ctx.var("OWNER_EMAIL") {
                Ok(v) => v.to_string(),
                Err(_) => "support@motorover.in".to_string(),
            };

            // 1. Email to Visitor
            let user_content = format!(
                "<h1>Hi {}</h1><p>Thanks for your interest in MotoRover.</p><p>You can download the requested information here: <a href='{}'>Download PDF</a></p><p>We will be in touch shortly.</p>",
                form_data.name, pdf_link
            );
            
            // 2. Email to Owner
            let owner_content = format!(
                "<h3>New Form Submission</h3><p><strong>Name:</strong> {}</p><p><strong>Email:</strong> {}</p><p><strong>Type:</strong> {}</p><p><strong>Message:</strong> {}</p>",
                form_data.name, form_data.email, form_data.form_type, form_data.message
            );

            if sendgrid_key != "placeholder" {
                let _ = utils::send_email(&sendgrid_key, &form_data.email, "Your MotoRover Information", &user_content).await;
                let _ = utils::send_email(&sendgrid_key, &owner_email, "New Lead: Website Form", &owner_content).await;
            } else {
                console_log!("Simulating email send to {} and {}", form_data.email, owner_email);
            }

            // Structured Logging (GDPR compliant - masked PII)
            let masked_email = if form_data.email.len() > 3 {
                format!("{}***", &form_data.email[0..3])
            } else {
                "***".to_string()
            };
            
            console_log!("{}", serde_json::to_string(&serde_json::json!({
                "event": "form_submission",
                "status": "success",
                "form_type": form_data.form_type,
                "masked_email": masked_email,
                "has_phone": form_data.phone.is_some()
            })).unwrap_or_default());

            Response::ok("Submission successful")?.with_headers(cors_headers)
        })
        .options("/api/submit", |_req, _ctx| {
            Response::empty().unwrap().with_headers(cors())
        })
        .run(req, env)
        .await
}

fn cors() -> Headers {
    let mut headers = Headers::new();
    headers.set("Access-Control-Allow-Origin", "*").unwrap();
    headers.set("Access-Control-Allow-Methods", "POST, OPTIONS").unwrap();
    headers.set("Access-Control-Allow-Headers", "Content-Type").unwrap();
    headers
}
