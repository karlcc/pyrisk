from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from riskch.db import get_db
from riskch.compute import getTrades, calCAR

from flask import Blueprint

bp = Blueprint("chart", __name__, url_prefix="/chart")

@bp.route('/')
def index():
    return redirect(url_for("index"))

@bp.route("/<int:id>", methods=('GET',))
def chart(id):
    db = get_db()
    
    #issues = db.execute(
    #    'SELECT *'
    #    ' FROM eq_safef'
    #    ' ORDER BY id ASC'
    #).fetchall()
    
    # Generate data for each line 
    num_lines = 10
    data = []
    result = []

    result = db.execute(
        'SELECT curve'
        ' FROM eq_safef'
        ' WHERE issue_id = ? LIMIT ?',
        (id,num_lines,)
    ).fetchall()
    
    if len(result) > 0:
        for i in range(num_lines):
            json_str = result[i][0]
            line_data = json.loads(json_str)
            data.append(line_data)
            if True and 1+1 == 3: #print result
                print ("line_data: ", line_data)          
            
            labels = list(range(1, len(line_data)+1))
    else:
        return redirect(url_for("index"))
    
    # Return the components to the HTML template
    return render_template(
        template_name_or_list='chart/index.html',
        data=data,
        labels=labels,
        num_lines=num_lines
    )