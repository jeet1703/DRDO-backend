from flask import Blueprint, jsonify, request
from mongo_config import records_collections
from bson import ObjectId
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

def get_collection(site):
    """Helper function to get the appropriate collection based on site"""
    return records_collections.get(site)

@dashboard_bp.route('/<site>/', methods=['GET'])
def get_records(site):
    """Get all records for a site"""
    records_collection = get_collection(site)
    if records_collection is None:
        return jsonify({"error": "Invalid site specified"}), 404
    
    try:
        records = list(records_collection.find({}))
        for idx, record in enumerate(records):
            # Convert ObjectId to string and add sequential id
            record['_id'] = str(record['_id'])
            record['id'] = idx + 1
            # Ensure all required fields exist
            record.setdefault('referenceNo', record['_id'])
            record.setdefault('comments', '')
            record.setdefault('status', 'In Process')
            
            # Add createdAt if it doesn't exist (using _id generation time as fallback)
            if 'createdAt' not in record:
                try:
                    record['createdAt'] = ObjectId(record['_id']).generation_time.isoformat()
                except:
                    record['createdAt'] = datetime.now().isoformat()
            
            # Set defaults for other fields as needed
            for field in ['nomenclature', 'institute', 'domainExpert', 'recommendation',
                        'researchVertical', 'cost', 'dateOfSanction', 'durationPDC',
                        'stakeHolderLab']:
                record.setdefault(field, '')
        
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard_bp.route('/<site>/update/<string:reference_no>', methods=['PUT'])
def update_record(site, reference_no):
    """Update a record's status or comments"""
    if reference_no == 'undefined':
        return jsonify({"error": "Invalid reference number"}), 400
        
    records_collection = get_collection(site)
    if records_collection is None:
        return jsonify({"error": "Invalid site specified"}), 404
    
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400
    
    try:
        # Prepare update data
        update_data = {}
        if 'status' in data:
            update_data['status'] = data['status']
        if 'comments' in data:
            update_data['comments'] = data['comments']
        
        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400
        
        # Try to update by _id first (converted from reference_no if it's an ObjectId string)
        try:
            obj_id = ObjectId(reference_no)
            result = records_collection.update_one(
                {'_id': obj_id},
                {'$set': update_data}
            )
        except:
            # If not an ObjectId, try updating by referenceNo
            result = records_collection.update_one(
                {'referenceNo': reference_no},
                {'$set': update_data}
            )
        
        if result.matched_count == 0:
            return jsonify({"error": "Record not found"}), 404
        
        return jsonify({
            "message": "Record updated successfully",
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard_bp.route('/<site>/add-comment/<string:reference_no>', methods=['POST'])
def add_comment(site, reference_no):
    """Add a comment to a record (appends to existing comments)"""
    if reference_no == 'undefined':
        return jsonify({"error": "Invalid reference number"}), 400
        
    records_collection = get_collection(site)
    if records_collection is None:
        return jsonify({"error": "Invalid site specified"}), 404
    
    data = request.json
    if not data or 'comment' not in data or not data['comment'].strip():
        return jsonify({"error": "No comment provided"}), 400
    
    try:
        # Find the record by _id or referenceNo
        try:
            obj_id = ObjectId(reference_no)
            record = records_collection.find_one({'_id': obj_id})
        except:
            record = records_collection.find_one({'referenceNo': reference_no})
        
        if not record:
            return jsonify({"error": "Record not found"}), 404
        
        # Prepare the new comment with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_comment = f"[{timestamp}] {data['comment'].strip()}"
        existing_comments = record.get('comments', '')
        updated_comments = f"{existing_comments}\n{new_comment}" if existing_comments else new_comment
        
        # Update the record
        try:
            obj_id = ObjectId(reference_no)
            result = records_collection.update_one(
                {'_id': obj_id},
                {'$set': {'comments': updated_comments.strip()}}
            )
        except:
            result = records_collection.update_one(
                {'referenceNo': reference_no},
                {'$set': {'comments': updated_comments.strip()}}
            )
        
        if result.matched_count == 0:
            return jsonify({"error": "Record not found"}), 404
        
        return jsonify({
            "message": "Comment added successfully",
            "comments": updated_comments
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@dashboard_bp.route('/<site>/delete/<string:reference_no>', methods=['DELETE'])
def delete_record(site, reference_no):
    """Delete a record"""
    if reference_no == 'undefined':
        return jsonify({"error": "Invalid reference number"}), 400
        
    records_collection = get_collection(site)
    if records_collection is None:
        return jsonify({"error": "Invalid site specified"}), 404
    
    try:
        try:
            obj_id = ObjectId(reference_no)
            result = records_collection.delete_one({'_id': obj_id})
        except:
            # If not an ObjectId, try deleting by referenceNo
            result = records_collection.delete_one({'referenceNo': reference_no})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Record not found"}), 404
        
        return jsonify({
            "message": "Record deleted successfully",
            "deleted_count": result.deleted_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500