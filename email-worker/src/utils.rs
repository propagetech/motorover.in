use worker::*;
use serde_json::json;

pub async fn verify_recaptcha(secret: &str, token: &str) -> Result<bool> {
    let client = reqwest::Client::new();
    // In a real worker environment, we should use worker::Fetch
    // But since we didn't include reqwest in Cargo.toml (I removed it in thought but let's check what I wrote),
    // I wrote: worker, serde, serde_json, console_error_panic_hook, regex.
    // So I must use worker::Fetch.
    
    let url = format!("https://www.google.com/recaptcha/api/siteverify?secret={}&response={}", secret, token);
    
    let mut headers = Headers::new();
    headers.set("Content-Type", "application/json")?;
    
    let request = Request::new_with_init(
        &url,
        &RequestInit {
            method: Method::Post,
            headers,
            ..Default::default()
        },
    )?;

    let mut response = Fetch::Request(request).send().await?;
    let body: serde_json::Value = response.json().await?;
    
    // Check score if using v3
    if let Some(success) = body.get("success").and_then(|v| v.as_bool()) {
        if success {
            if let Some(score) = body.get("score").and_then(|v| v.as_f64()) {
                return Ok(score >= 0.5); // Threshold
            }
            return Ok(true);
        }
    }
    
    Ok(false)
}

pub async fn send_email(
    api_key: &str,
    to_email: &str,
    subject: &str,
    content: &str,
) -> Result<()> {
    // Example using SendGrid API
    let url = "https://api.sendgrid.com/v3/mail/send";
    
    let body = json!({
        "personalizations": [{
            "to": [{ "email": to_email }]
        }],
        "from": { "email": "noreply@motorover.in" },
        "subject": subject,
        "content": [{
            "type": "text/html",
            "value": content
        }]
    });

    let mut headers = Headers::new();
    headers.set("Authorization", &format!("Bearer {}", api_key))?;
    headers.set("Content-Type", "application/json")?;

    let request = Request::new_with_init(
        url,
        &RequestInit {
            method: Method::Post,
            headers,
            body: Some(wasm_bindgen::JsValue::from_str(&body.to_string())),
            ..Default::default()
        },
    )?;

    let response = Fetch::Request(request).send().await?;
    
    if response.status_code() >= 200 && response.status_code() < 300 {
        Ok(())
    } else {
        Err(Error::from(format!("Failed to send email: {}", response.status_code())))
    }
}

pub fn get_pdf_link(form_type: &str) -> &'static str {
    match form_type {
        "tour_inquiry" => "https://motorover.in/assets/brochures/tour-catalog.pdf",
        "booking" => "https://motorover.in/assets/docs/booking-terms.pdf",
        _ => "https://motorover.in/assets/docs/general-info.pdf",
    }
}
