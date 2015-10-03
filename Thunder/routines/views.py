from __future__ import absolute_import
import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Routine, Exercise

from .serializers import RoutineSerializer, ExerciseSerializer, FullRoutineSerializer


@login_required
def routineView(request):
    return render(request, 'routines/routine.html')


# API #########################################################################

@api_view(['POST'])
def routineCreate(request):

    serializer = RoutineSerializer(data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def exerciseCreate(request):

    serializer = ExerciseSerializer(data=request.data)
    serializer.initial_data['routine'] = Routine.objects.filter(name=serializer.initial_data['routine'])[:1]

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def routineGet(request):

    exercises = Exercise.objects.get(routine=request.data['routine'], routine__user=request.user)
    serializer = ExerciseSerializer(exercises, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def getRoutines(request):

    routines = Routine.objects.all()

    userPk = request.GET.get("user", None)

    if userPk:

        routines = Routine.objects.filter(user__id=userPk)
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getRoutine(request):

    userPk = request.GET.get("user", None)

    routineName = request.GET.get("routine", None)

    if userPk and routineName:

        exercises = Exercise.objects.filter(routine__name=routineName).order_by('position')

        fullSerializer = FullRoutineSerializer(exercises, many=True)

        return Response(fullSerializer.data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def postRoutine(request):

    try:
        routine = Routine.objects.get(name=request.data['name'], user__id=request.data['user'])
        routineSerializer = RoutineSerializer(routine, data=request.data)

    except Routine.DoesNotExist:
        routineSerializer = RoutineSerializer(data=request.data)

    if routineSerializer.is_valid():
        routineSerializer.save()
        return Response(routineSerializer.data, status=status.HTTP_202_ACCEPTED)

    else:
        return Response(routineSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def postRoutineDelete(request):

    try:
        routine = Routine.objects.get(name=request.data['old_name'], user__id=request.data['user'])
        routine.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    except Routine.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def postExercises(request):

    # Convert routine name to ID
    for exercise in request.data:
        routineID = Routine.objects.get(name=exercise['routine']).id
        exercise['routine'] = routineID

    exercisesSerializer = ExerciseSerializer(data=request.data, many=True)

    if exercisesSerializer.is_valid():
        exercisesSerializer.save()
        return Response(exercisesSerializer.data, status=status.HTTP_202_ACCEPTED)

    else:
        print(exercisesSerializer.errors)
        return Response(exercisesSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def postExercise(request):

    try:
        exercise = Exercise.objects.get(name=request.data['name'], position=request.data['position'])
        routineID = Routine.objects.get(name=request.data['routine']).id
        request.data['routine'] = routineID
        exerciseSerializer = ExerciseSerializer(exercise, data=request.data)

    except Exercise.DoesNotExist:
        routineID = Routine.objects.get(name=request.data['routine']).id
        request.data['routine'] = routineID
        exerciseSerializer = ExerciseSerializer(data=request.data)

    if exerciseSerializer.is_valid():
        exerciseSerializer.save()
        return Response(exerciseSerializer.data, status=status.HTTP_202_ACCEPTED)

    else:
        print(exerciseSerializer.errors)
        return Response(exerciseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
