
# Get the Flask Files Required
from flask import Blueprint, request, url_for, redirect, render_template, flash, jsonify

# Journalist firestore collection
from system.firstoredb import brandlinkdetails_ref
# Journalist firestore collection
from system.firstoredb import brandlinks_ref
# Journalist firestore collection
from system.firstoredb import brandsearchquery_ref
# Journalist firestore collection
from system.firstoredb import brandstopwords_ref

# Set Blueprint’s name https://realpython.com/flask-blueprint/
brandsblue = Blueprint('brandsblue', __name__)

# Check if Logged in
from modules.auth.auth import login_is_required

### Brand
###  Brand Section

#
# API Route add a searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandsearchqueryadd", methods=['GET'], endpoint='brandsearchqueryadd')
@login_is_required
def brandsearchqueryadd():
    return render_template('brandtracking/brandsearchqueryadd.html', **locals())
    
#
# API Route add a searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandsearchquerycreate", methods=['POST'], endpoint='brandsearchquerycreate')
@login_is_required
def brandsearchquerycreate():
    try:
        data = {
            u'active': False,
            u'queryterm': request.form.get('queryterm'),
            u'querytype': request.form.get('querytype'),
            u'language': request.form.get('language')
        }
        
        brandsearchquery_ref.document().set(data)
        flash('Data Succesfully Submitted')
        return redirect(url_for('brandsblue.brandsearchquery'))
    except Exception as e:
        flash(f'An Error Occured: ' + str(e))
        return redirect(url_for('brandsblue.brandsearchquery'))
#
# API Route list all or a speific counter by ID - requires json file body with id and count
#
@brandsblue.route("/brandsearchquery", methods=['GET'], endpoint='brandsearchquery')
@login_is_required
def brandsearchquery():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')    
        if id:
            brandsearchquery = brandsearchquery_ref.document(id).get()
            return jsonify(u'{}'.format(brandsearchquery.to_dict()['count'])), 200
        else:
            all_brandsearchquerylinks = []     
            for doc in brandsearchquery_ref.stream():
                don = doc.to_dict()
                don["docid"] = doc.id
                all_brandsearchquerylinks.append(don)
            
            return render_template('brandtracking/brandsearchquery.html', output=all_brandsearchquerylinks)
    except Exception as e:
        return f"An Error Occured: {e}"

#
# API Route list all or a speific searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandsearchqueryedit", methods=['GET'], endpoint='brandsearchqueryedit')
@login_is_required
def brandsearchqueryedit():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        brandsearchquerylink = brandsearchquery_ref.document(id).get()
        output=brandsearchquerylink.to_dict()
        output["docid"] = id
        return render_template('brandtracking/brandsearchqueryedit.html', ngo=output)
    except Exception as e:
        return f"An Error Occured: {e}"
    
#
# API Route Delete a csearchlink by ID /delete?id=<id>
# API Enfpoint /delete?id=<id>
#
@brandsblue.route("/brandsearchquerydelete", methods=['GET', 'DELETE'], endpoint='brandsearchquerydelete')
@login_is_required
def brandsearchquerydelete():
    try:
        # Check for ID in URL query
        id = request.args.get('id')
        brandsearchquery_ref.document(id).delete()
        return redirect(url_for('brandsblue.brandsearchquery'))
    except Exception as e:
        return f"An Error Occured: {e}"
    
#
# API Route Update a counter by ID - requires json file body with id and count
# API endpoint /update?id=<id>&count=<count>
#
@brandsblue.route("/brandsearchqueryupdate", methods=['POST', 'PUT'], endpoint='brandsearchqueryupdate')
@login_is_required
def brandsearchqueryupdate():
    try:
        id = request.form['id']
        brandsearchquery_ref.document(id).update(request.form)
        return redirect(url_for('brandsblue.brandsearchquery'))
    except Exception as e:
        return f"An Error Occured: {e}"
#
# API Route Delete a csearchlink by ID /delete?id=<id>
# API Enfpoint /delete?id=<id>
#
@brandsblue.route("/brandsearchqueryactive", methods=['GET', 'DELETE'], endpoint='brandsearchqueryactive')
@login_is_required
def brandsearchqueryactive():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        brandsearchquerylink = brandsearchquery_ref.document(id).get()
        brandsearchqueryactive = brandsearchquerylink.to_dict()
        
        ## Update flag that translation done
        if brandsearchqueryactive['active'] == True:
             data = {
                u'active': False,
            }
        else:            
            data = {
                u'active': True,
            }
        brandsearchquery_ref.document(id).update(data)
        
        return redirect(url_for('brandsblue.brandsearchquery'))
    except Exception as e:
        return f"An Error Occured: {e}"

#
# API Route add a counter by ID - requires json file body with id and count
#
@brandsblue.route("/brandstopwordsadd", methods=['GET'], endpoint='brandstopwordsadd')
@login_is_required
def brandstopwordsadd():
    return render_template('brandtracking/brandstopwordsadd.html', **locals())
    
#
# API Route add a counter by ID - requires json file body with id and count
#
@brandsblue.route("/brandstopwordscreate", methods=['POST'], endpoint='brandstopwordscreate')
@login_is_required
def brandstopwordscreate():
    try:
        data = {
            u'active': False,
            u'querykeywords': request.form.get('querykeywords'),
            u'language': request.form.get('language')
        }
        
        brandstopwords_ref.document().set(data)
        flash('Data Succesfully Submitted')
        return redirect(url_for('brandsblue.brandstopwords'))
    except Exception as e:
        flash('An Error Occvured')
        return f"An Error Occured: {e}"
#
# API Route list all or a speific counter by ID - requires json file body with id and count
#
@brandsblue.route("/brandstopwords", methods=['GET'], endpoint='brandstopwords')
@login_is_required
def brandstopwords():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')    
        if id:
            brandstopwords = brandstopwords_ref.document(id).get()
            return jsonify(u'{}'.format(counter.to_dict()['count'])), 200
        else:
            all_brandstopwords = []     
            for doc in brandstopwords_ref.stream():
                don = doc.to_dict()
                don["docid"] = doc.id
                all_brandstopwords.append(don)
            return render_template('brandtracking/brandstopwords.html', output=all_brandstopwords)
    except Exception as e:
        return f"An Error Occured: {e}"

#
# API Route list all or a speific counter by ID - requires json file body with id and count
#
@brandsblue.route("/brandstopwordsedit", methods=['GET'], endpoint='brandstopwordsedit')
@login_is_required
def brandstopwordsedit():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        brandstopwords = brandstopwords_ref.document(id).get()
        output=brandstopwords.to_dict()
        output["docid"] = id
        return render_template('brandtracking/brandstopwordsedit.html', ngo=output)
    except Exception as e:
        return f"An Error Occured: {e}"
    
#
# API Route Delete a counter by ID /delete?id=<id>
# API Enfpoint /delete?id=<id>
#
@brandsblue.route("/brandstopwordsdelete", methods=['GET', 'DELETE'], endpoint='brandstopwordsdelete')
@login_is_required
def brandstopwordsdelete():
    try:
        # Check for ID in URL query
        id = request.args.get('id')
        brandstopwords_ref.document(id).delete()
        return redirect(url_for('brandsblue.brandstopwords'))
    except Exception as e:
        return f"An Error Occured: {e}"

#
# API Route Update a counter by ID - requires json file body with id and count
# API endpoint /update?id=<id>&count=<count>
#
@brandsblue.route("/brandstopwordsupdate", methods=['POST', 'PUT'], endpoint='brandstopwordsupdate')
@login_is_required
def brandstopwordsupdate():
    try:
        id = request.form['id']
        brandstopwords_ref.document(id).update(request.form)
        return redirect(url_for('brandsblue.brandstopwords'))
    except Exception as e:
        return f"An Error Occured: {e}"
    
#
# API Route Delete a csearchlink by ID /delete?id=<id>
# API Enfpoint /delete?id=<id>
#
@brandsblue.route("/brandstopwordsactive", methods=['GET', 'DELETE'], endpoint='brandstopwordsactive')
@login_is_required
def brandstopwordsactive():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        brandstopwords = brandstopwords_ref.document(id).get()
        brandstopwordsactive = brandstopwords.to_dict()
        
        ## Update flag that translation done
        if brandstopwordsactive['active'] == True:
             data = {
                u'active': False,
            }
        else:            
            data = {
                u'active': True,
            }
        brandstopwords_ref.document(id).update(data)
        
        return redirect(url_for('brandsblue.brandstopwords'))
    except Exception as e:
        return f"An Error Occured: {e}"
    
###  Brand Links Section

#
# API Route add a searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandlinksadd", methods=['GET'], endpoint='brandlinksadd')
@login_is_required
def brandlinksadd():
    return render_template('brandtracking/brandlinksadd.html', **locals())
    
#
# API Route add a searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandlinkscreate", methods=['POST'], endpoint='brandlinkscreate')
@login_is_required
def brandlinkscreate():
    try:
        data = {
            u'active': False,
            u'keyword': request.form.get('keyword'),
            u'language': request.form.get('language'),
            u'campaign': request.form.get('campaign'),
            u'country': request.form.get('country')
        }
        
        brandlinks_ref.document().set(data)
        flash('Data Succesfully Submitted')
        return redirect(url_for('brandsblue.brandlinks'))
    except Exception as e:
        flash(f'An Error Occured: ' + str(e))
        return redirect(url_for('brandsblue.brandlinks'))
#
# API Route list all or a speific counter by ID - requires json file body with id and count
#
@brandsblue.route("/brandlinks", methods=['GET'], endpoint='brandlinks')
@login_is_required
def brandlinks():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')    
        if id:
            brandlinks = brandlinks_ref.document(id).get()
            return jsonify(u'{}'.format(brandlinks.to_dict()['count'])), 200
        else:
            all_brandlinks = []     
            for doc in brandlinks_ref.stream():
                don = doc.to_dict()
                don["docid"] = doc.id
                all_brandlinks.append(don)
            
            return render_template('brandtracking/brandlinks.html', output=all_brandlinks)
    except Exception as e:
        return f"An Error Occured: {e}"

#
# API Route list all or a speific searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandlinksedit", methods=['GET'], endpoint='brandlinksedit')
@login_is_required
def brandlinksedit():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        brandlinks = brandlinks_ref.document(id).get()
        return render_template('brandtracking/brandlinksedit.html', ngo=brandlinks.to_dict())
    except Exception as e:
        return f"An Error Occured: {e}"
    
#
# API Route Delete a csearchlink by ID /delete?id=<id>
# API Enfpoint /delete?id=<id>
#
@brandsblue.route("/brandlinksdelete", methods=['GET', 'DELETE'], endpoint='brandlinksdelete')
@login_is_required
def brandsearchquerydelete():
    try:
        # Check for ID in URL query
        id = request.args.get('id')
        brandlinks_ref.document(id).delete()
        return redirect(url_for('brandsblue.brandlinks'))
    except Exception as e:
        return f"An Error Occured: {e}"

#
# API Route Delete a csearchlink by ID /delete?id=<id>
# API Enfpoint /delete?id=<id>
#
@brandsblue.route("/brandlinksactive", methods=['GET', 'DELETE'], endpoint='brandlinksactive')
@login_is_required
def brandlinksactive():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        brandlinks = brandlinks_ref.document(id).get()
        brandlinksactive = brandlinks.to_dict()
        
        ## Update flag that translation done
        if brandlinksactive['status'] == True:
             data = {
                u'status': False,
            }
        else:            
            data = {
                u'status': True,
            }
        brandlinks_ref.document(id).update(data)
        
        return redirect(url_for('brandsblue.brandlinks'))
    except Exception as e:
        return f"An Error Occured: {e}"

###  Brand Section
#
# API Route add a searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandmap", methods=['GET'], endpoint='brandmap')
@login_is_required
def brandmap():
    return render_template('brandtracking/brandmap.html', **locals())


###  Brand Links Details Section

#
# API Route add a searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandlinkdetailsadd", methods=['GET'], endpoint='brandlinkdetailsadd')
@login_is_required
def brandlinkdetailsadd():
    return render_template('brandtracking/brandlinkdetailsadd.html', **locals())
    
#
# API Route add a searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandlinkdetailscreate", methods=['POST'], endpoint='brandlinkdetailscreate')
@login_is_required
def brandlinkdetailscreate():
    try:
        data = {
            u'active': False,
            u'keyword': request.form.get('keyword'),
            u'language': request.form.get('language'),
            u'campaign': request.form.get('campaign'),
            u'country': request.form.get('country')
        }
        
        brandlinkdetails_ref.document().set(data)
        flash('Data Succesfully Submitted')
        return redirect(url_for('brandblue.brandlinkdetails'))
    except Exception as e:
        flash(f'An Error Occured: ' + str(e))
        return redirect(url_for('brandsblue.brandlinkdetails'))
#
# API Route list all or a speific counter by ID - requires json file body with id and count
#
@brandsblue.route("/brandlinkdetails", methods=['GET'], endpoint='brandlinkdetails')
@login_is_required
def brandlinkdetails():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')    
        if id:
            brandlinkdetails = brandlinkdetails_ref.document(id).get()
            return render_template('brandtracking/brandlinkdetail.html', output=brandlinkdetails.to_dict())
        else:
            all_brandlinkdetails = []     
            for doc in brandlinks_ref.stream():
                don = doc.to_dict()
                don["docid"] = doc.id
                all_brandlinkdetails.append(don)
            
            return render_template('brandtracking/brandlinkdetails.html', output=all_brandlinkdetails)
    except Exception as e:
        return f"An Error Occured: {e}"

#
# API Route list all or a speific searchlink by ID - requires json file body with id and count
#
@brandsblue.route("/brandlinkdetailsedit", methods=['GET'], endpoint='brandlinkdetailsedit')
@login_is_required
def brandlinksedit():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        brandlinkdetails = brandlinkdetails_ref.document(id).get()
        return render_template('brandtracking/brandlinkdetailsedit.html', ngo=brandlinkdetails.to_dict())
    except Exception as e:
        return f"An Error Occured: {e}"
    
#
# API Route Delete a csearchlink by ID /delete?id=<id>
# API Enfpoint /delete?id=<id>
#
@brandsblue.route("/brandlinkdetailsdelete", methods=['GET', 'DELETE'], endpoint='brandlinkdetailsdelete')
@login_is_required
def brandlinkdetailsdelete():
    try:
        # Check for ID in URL query
        id = request.args.get('id')
        brandlinkdetails_ref.document(id).delete()
        return redirect(url_for('brandsblue.brandlinkdetails'))
    except Exception as e:
        return f"An Error Occured: {e}"

#
# API Route Delete a csearchlink by ID /delete?id=<id>
# API Enfpoint /delete?id=<id>
#
@brandsblue.route("/brandlinkdetailsactive", methods=['GET', 'DELETE'], endpoint='brandlinkdetailsactive')
@login_is_required
def brandlinkdetailsactive():
    try:
        # Check if ID was passed to URL query
        id = request.args.get('id')
        brandlinkdetails = brandlinkdetails_ref.document(id).get()
        brandlinkdetailsactive = brandlinkdetails.to_dict()
        
        ## Update flag that translation done
        if brandlinkdetailsactive['active'] == True:
             data = {
                u'active': False,
            }
        else:            
            data = {
                u'active': True,
            }
        brandlinkdetails_ref.document(id).update(data)
        
        return redirect(url_for('brandsblue.brandlinkdetails'))
    except Exception as e:
        return f"An Error Occured: {e}"
