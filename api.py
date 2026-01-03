"""REST API endpoints for Odoo integration."""
from __future__ import annotations

import os
from functools import wraps
from flask import request, jsonify
from model_client import ModelClient
from prompts import build_document_prompt


def require_api_key(f):
    """Decorator to require API key authentication for API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.environ.get('ODOO_API_KEY')
        
        if not expected_key:
            return jsonify({'error': 'API key authentication not configured'}), 500
        
        if not api_key or api_key != expected_key:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        
        return f(*args, **kwargs)
    return decorated_function


def register_api_routes(app, model_client: ModelClient):
    """Register API routes for Odoo integration."""
    
    @app.route('/api/v1/health', methods=['GET'])
    def api_health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'service': 'AIbot',
            'version': '1.0'
        })
    
    @app.route('/api/v1/generate', methods=['POST'])
    @require_api_key
    def api_generate():
        """Generate AI response for a given prompt.
        
        Request body:
        {
            "prompt": "Your question or prompt",
            "document_type": "General" (optional),
            "jurisdiction": "Federal" (optional),
            "context": {} (optional additional context)
        }
        """
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing required field: prompt'}), 400
        
        prompt_text = data.get('prompt', '').strip()
        doc_type = data.get('document_type', 'General')
        jurisdiction = data.get('jurisdiction', 'Federal')
        context = data.get('context', {})
        
        if not prompt_text:
            return jsonify({'error': 'Prompt cannot be empty'}), 400
        
        # Build the full prompt
        full_prompt = build_document_prompt(
            doc_type=doc_type,
            jurisdiction=jurisdiction,
            user_text=prompt_text
        )
        
        # Add context if provided
        if context:
            context_str = "\n\nAdditional Context:\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"
            full_prompt += context_str
        
        try:
            response = model_client.generate(full_prompt)
            return jsonify({
                'success': True,
                'response': response,
                'prompt': prompt_text,
                'document_type': doc_type,
                'jurisdiction': jurisdiction
            })
        except Exception as exc:
            return jsonify({
                'success': False,
                'error': str(exc)
            }), 500
    
    @app.route('/api/v1/generate/product-description', methods=['POST'])
    @require_api_key
    def api_generate_product_description():
        """Generate product description.
        
        Request body:
        {
            "product_name": "Product name",
            "category": "Product category" (optional),
            "features": ["feature1", "feature2"] (optional),
            "target_audience": "Target audience" (optional)
        }
        """
        data = request.get_json()
        
        if not data or 'product_name' not in data:
            return jsonify({'error': 'Missing required field: product_name'}), 400
        
        product_name = data.get('product_name')
        category = data.get('category', '')
        features = data.get('features', [])
        target_audience = data.get('target_audience', '')
        
        # Build product description prompt
        prompt = f"Generate a compelling product description for:\n\n"
        prompt += f"Product Name: {product_name}\n"
        if category:
            prompt += f"Category: {category}\n"
        if features:
            prompt += f"Key Features:\n"
            for feature in features:
                prompt += f"- {feature}\n"
        if target_audience:
            prompt += f"Target Audience: {target_audience}\n"
        
        prompt += "\nPlease create a professional, engaging product description that highlights the key benefits and features."
        
        try:
            response = model_client.generate(prompt)
            return jsonify({
                'success': True,
                'description': response,
                'product_name': product_name
            })
        except Exception as exc:
            return jsonify({
                'success': False,
                'error': str(exc)
            }), 500
    
    @app.route('/api/v1/generate/email', methods=['POST'])
    @require_api_key
    def api_generate_email():
        """Generate email content.
        
        Request body:
        {
            "purpose": "Email purpose (e.g., 'customer follow-up', 'sales inquiry')",
            "recipient_name": "Recipient name" (optional),
            "context": "Additional context" (optional),
            "tone": "professional|friendly|formal" (optional)
        }
        """
        data = request.get_json()
        
        if not data or 'purpose' not in data:
            return jsonify({'error': 'Missing required field: purpose'}), 400
        
        purpose = data.get('purpose')
        recipient_name = data.get('recipient_name', '')
        context = data.get('context', '')
        tone = data.get('tone', 'professional')
        
        # Build email generation prompt
        prompt = f"Generate a {tone} email for the following purpose:\n\n"
        prompt += f"Purpose: {purpose}\n"
        if recipient_name:
            prompt += f"Recipient: {recipient_name}\n"
        if context:
            prompt += f"Context: {context}\n"
        
        prompt += "\nPlease create a well-structured email with appropriate greeting, body, and closing."
        
        try:
            response = model_client.generate(prompt)
            return jsonify({
                'success': True,
                'email_content': response,
                'purpose': purpose
            })
        except Exception as exc:
            return jsonify({
                'success': False,
                'error': str(exc)
            }), 500
    
    @app.route('/api/v1/generate/document', methods=['POST'])
    @require_api_key
    def api_generate_document():
        """Generate legal or business document.
        
        Request body:
        {
            "document_type": "Contract|Agreement|Policy|etc",
            "jurisdiction": "Federal|State|etc" (optional),
            "parties": ["Party 1", "Party 2"] (optional),
            "terms": "Key terms and conditions" (optional),
            "additional_info": "Any additional information" (optional)
        }
        """
        data = request.get_json()
        
        if not data or 'document_type' not in data:
            return jsonify({'error': 'Missing required field: document_type'}), 400
        
        doc_type = data.get('document_type')
        jurisdiction = data.get('jurisdiction', 'Federal')
        parties = data.get('parties', [])
        terms = data.get('terms', '')
        additional_info = data.get('additional_info', '')
        
        # Build document generation prompt
        prompt = f"Generate a {doc_type} document with the following details:\n\n"
        prompt += f"Jurisdiction: {jurisdiction}\n"
        if parties:
            prompt += f"Parties Involved:\n"
            for i, party in enumerate(parties, 1):
                prompt += f"{i}. {party}\n"
        if terms:
            prompt += f"\nKey Terms:\n{terms}\n"
        if additional_info:
            prompt += f"\nAdditional Information:\n{additional_info}\n"
        
        prompt += "\nPlease create a professional, legally sound document template."
        
        try:
            response = model_client.generate(prompt)
            return jsonify({
                'success': True,
                'document_content': response,
                'document_type': doc_type
            })
        except Exception as exc:
            return jsonify({
                'success': False,
                'error': str(exc)
            }), 500
