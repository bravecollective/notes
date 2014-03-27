$(document).ready(function () {
    $('#deleteModal').on('show', function() {
        var id = $(this).data('id'),
            removeBtn = $(this).find('.danger');
    })

    $('.confirm-delete').on('click', function(e) {
        e.preventDefault();

        var id = $(this).data('id');
        var form = $(this).data('form');
        var field = $(this).data('field');
        $('#deleteModal').data('id', id).data('form', form).data('field', field).modal('show');
    });

    $('#btnYes').click(function() {
        // handle deletion here
        var id = $('#deleteModal').data('id');
        var form = $('#deleteModal').data('form');
        var field = $('#deleteModal').data('field');
        $(field).val(id);
        $(form).submit()
        $('#deleteModal').modal('hide');
    });
});