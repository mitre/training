let refresher = setInterval(refresh, 15000);
$('.section-profile').bind('destroyed', function() {
    clearInterval(refresher);
});
$(document).ready(function () {
    refresh();
});

function loadCertification(){
    function loadCert(data){
        data[0].badges.forEach(function(badge) {
            let template = $("#badge-template").clone();
            template.attr("id", "badge-" + badge.name);
            template.find('#badge-name').text(badge.name);
            template.find('#badge-icon').attr('src', '/training/img/badges/'+badge.name+'.png');
            template.show();
            $('#badges').append(template);
        });
        refresh();
    }
    let selectedCert = $('#certification-name option:selected').attr('value');
    stream('Hover over each flag to get adversary emulation tips & tricks!');
    setCertDescription(selectedCert);
    $('#badges').empty();
    restRequest('POST', {"index":"certifications","name":selectedCert}, loadCert)
}

function setCertDescription(selectedCert) {
    $.each(certificates, function(index, cert) {
        if (cert.name == selectedCert) {
            $('#training-cert-description-modal').find('h3').text(cert.name);
            $('#training-cert-description-modal').find('p').html(cert.description);
            return false; //break loop
        }
    });
}

function refresh(){
    function update(data){
        let completedBadges = 0;
        let code = [];
        let flags = $('#flags');
        flags.empty();

        console.log(data.badges)

        badgeLoop:
        for (var badgeIdx in data.badges) {
            var badge = data.badges[badgeIdx];
            let badgeComplete = 0;
            let b = $('#badge-'+badge.name);
            b.find('.badge-icon').addClass('badge-in-progress');
            b.attr('status', 'progress');
            console.log(badgeIdx)
            for (var flagIdx in badge.flags) {
                var flag = badge.flags[flagIdx];
                let flagHTML = createFlagHTML(badge, flag);
                if(flag.completed) {
                    flagHTML.find('#flag-status').html('&#x2705;');
                    badgeComplete += 1;
                    code.push(flag.code);
                    flags.append(flagHTML);
                } else {
                    flagHTML.find('#flag-status').html('&#10060;');
                    flags.append(flagHTML);
                    break badgeLoop; //show only the next incomplete flag
                }
            }
            if(badgeComplete === badge.flags.length) {
                b.find('.badge-icon').removeClass('badge-in-progress');
                b.find('.badge-icon').addClass('badge-completed');
                b.attr('status', 'completed');
                completedBadges += 1
            }
        }
        showRelevantFlags();
        displayCert(code, completedBadges, data.badges.length);
    }

    let selectedCert = $('#certification-name option:selected').attr('value');
    if(!selectedCert){
        return;
    }
    $('#training-disclaimers').hide();
    restRequest('POST', {"name":selectedCert, "answers":getAnswers()}, update, '/plugin/training/flags');
}

function createFlagHTML(badge, flag) {
    let template = $("#flag-template").clone();
    template.removeAttr('id');
    template.attr('badge', badge.name);
    template.find('#flag-number').html('&#127937 ' + flag.number);
    template.find('#flag-name').text(flag.name);
    template.find("#flag-challenge").text(flag.challenge);
    if (flag.flag_type) {
        addAnswerOptions(flag, template);
    }
    if (flag.extra_info == null || flag.extra_info == "") {
        template.find(".flip-card-inner").attr('data-flip', 'false');
    } else {
        template.find("#flag-info").text(flag.extra_info);
    }
    template.find("#flag-completed-ts").text(flag.completed_ts);
    return template
}

function addAnswerOptions(flag, template) {
    template.find("#flag-answer").show();
    template.find("#flag-answer").attr("id", "flag-answer-" + flag.number);
    template.find("#flag-answer-" + flag.number).addClass("flag-answer");
    switch (flag.flag_type) {
        case "multiplechoice":
            let mcType = ''
            if (flag.multi_select) {
                mcType = 'checkbox'
            } else {
                mcType = 'radio'
            }
            flag.options.forEach(function(o) {
                let btnSet = "mult-" + flag.number;
                let radioHTML = "<label><input type='" + mcType + "' name='" + btnSet + "' value='" + o + "'>" + o + "</label><br>";
                template.find("#flag-answer-" + flag.number).append(radioHTML);
            })
            break;
        case "fillinblank":
                template.find("#flag-answer-" + flag.number).append("<input style='width: 95%; text-align: left'></input>");
            break;
        default:
            stream("Unknown flag type provided");
    }

}

function showRelevantFlags() {
    let flags = $('#flags');
    let selected = $('#badges').find('.selected-badge');
    if (selected.length) {
        var badge_name = selected.find('#badge-name').text();
        flags.find('li').each(function() {
            if ($(this).attr('badge') === badge_name) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    } else {
        flags.find('li').each(function() {
            $(this).show();
        });
    }
}

function getAnswers() {
    let answers = {}
    $(".flag-answer").each(function(i, set) {
        if ($(set).parent().find("#flag-status").html().charCodeAt(0) == 9989) {
//        skip flags that have already been completed
            return;
        }
        let flagNum = $(set).attr("id").split("-")[2];
        let answer = $(set).find("input:checked");
        if (answer.length > 1) {
            let arr = [];
            answer.each(function(idx, a) {
                arr.append(a.value)
            })
            answer = arr
        }
        else if (answer.length == 1) {
            answer = answer.val();
        }
        else {
            answer = $(set).find("input").val();
        }
        answers[flagNum] = answer;
    })
    return answers;
}

function selectBadge(element) {
    if ($(element).hasClass('selected-badge')) {
        $(element).removeAttr('class');
        $(element).find('.badge-icon').removeAttr('id');
        showRelevantFlags();
    } else if ($(element).attr('status')){
        $('#badges').find('li').each(function() {
            $(this).removeAttr('class');
            $(this).find('.badge-icon').removeAttr('id');
        });
        $(element).attr('class', 'selected-badge');
        $(element).find('.badge-icon').attr('id', 'selected-badge-icon');
        showRelevantFlags();
    }
}

function displayCert(code, completedBadges, totalBadges) {
    if(completedBadges === totalBadges) {
        code = code.sort(function(a, b) {
            return a.toString().length - b.toString().length;
        });
        code = code.join(' ');
        document.getElementById("alert-modal").style.display="block";
        let alert_text = "Congratulations! You've completed the certification! The code for the certification is below:\n\n" + btoa(code);
        $('#alert-text').html(alert_text).css('white-space', 'pre-wrap');
        $('#alert-text').html(alert_text).css('word-wrap', 'break-word');
        clearInterval(refresher);
    }
}